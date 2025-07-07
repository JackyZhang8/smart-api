import asyncio
import json
import websockets
import argparse
from datetime import datetime
WEBSOCKET_HOST = "0.0.0.0"
WEBSOCKET_PORT = 8765
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NTQyODE5MDYsImlhdCI6MTc1MTY4OTkwNiwibm90ZSI6InRlc3QgdG9rZW4ifQ.HYLhKxHB5QzpJLNjPnDf0tES7jrv_KSJY4-R6t8JE3Y"

class TradeSignalClient:
    def __init__(self, test_mode=False):
        self.uri = f"ws://{WEBSOCKET_HOST}:{WEBSOCKET_PORT}"
        self.test_mode = test_mode
    
    async def connect_and_receive(self):
        """Connect to WebSocket server and receive trade signals"""
        print(f"Connecting to WebSocket server at {self.uri}")
        
        # Add authentication token in the header with Bearer scheme
        try:
            # Create a connection with headers - headers must be a dictionary
            headers = {'Authorization': f"Bearer {TOKEN}"}
            async with websockets.connect(self.uri, additional_headers=headers, proxy=None) as websocket:
                print("Connected to WebSocket server")
                
                # If in test mode, send a test command
                if self.test_mode:
                    print("Sending test command to server...")
                    await websocket.send("test")
                    print("Test command sent. Waiting for response...")
                
                # Keep receiving messages
                while True:
                    try:
                        message = await websocket.recv()
                        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        
                        # Parse the message
                        try:
                            signal = json.loads(message)
                            signal_type = signal.get('type', 'unknown')
                            symbol = signal.get('content', {}).get('symbol', 'unknown')
                            price = signal.get('content', {}).get('price', 0)
                            is_test = signal.get('is_test', False)
                            
                            # Format and print the signal
                            test_indicator = "[TEST] " if is_test else ""
                            if signal_type == 'buy':
                                print(f"[{current_time}] {test_indicator}📈 BUY SIGNAL: {symbol} at ${price}")
                            elif signal_type == 'sell':
                                print(f"[{current_time}] {test_indicator}📉 SELL SIGNAL: {symbol} at ${price}")
                            else:
                                print(f"[{current_time}] {test_indicator}Unknown signal type: {signal}")
                            
                            # If this was a test response and we're in test mode, exit after receiving it
                            if is_test and self.test_mode:
                                print("Test completed successfully. Exiting.")
                                return
                        
                        except json.JSONDecodeError:
                            print(f"[{current_time}] Received non-JSON message: {message}")
                    
                    except websockets.exceptions.ConnectionClosed:
                        print("Connection to server closed")
                        break
        
        except Exception as e:
            print(f"Error connecting to WebSocket server: {e}")
    
    def run(self):
        """Run the client"""
        try:
            asyncio.run(self.connect_and_receive())
        except KeyboardInterrupt:
            print("\nClient stopped by user")
        except Exception as e:
            print(f"Error in client: {e}")

if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="WebSocket client for trade signals")
    
    # Create mutually exclusive group for run modes
    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument(
        "--run", 
        action="store_true", 
        help="Run in normal mode: receive trade signals continuously"
    )
    mode_group.add_argument(
        "--test", 
        action="store_true", 
        help="Run in test mode: send a test command and exit after receiving response"
    )
    
    args = parser.parse_args()
    
    # Create and run the client
    client = TradeSignalClient(test_mode=args.test)
    client.run()
