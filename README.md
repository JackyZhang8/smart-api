# WebSocket 集成指南

本文档介绍如何对接 WebSocket 服务，获取实时交易信号和市场数据，适用于客户端开发者集成。

## 连接说明

### WebSocket 地址

```
wss://{host}:{port}
```
将 `{host}` 和 `{port}` 替换为实际服务器的主机和端口。

### 认证

WebSocket 连接需要使用 Bearer Token 进行认证。在建立连接时，需要在 HTTP 头中添加 `Authorization` 字段。

认证头格式：
```
Authorization: Bearer {your_token}
```

- `{your_token}` 需要替换为有效的访问令牌
- 如果认证失败，连接将会被服务器立即关闭

获取 Token 的方式请参考 API 文档或联系系统管理员。

## 消息格式

### 服务器推送消息（JSON 格式）

```json
{
  "type": "buy|sell",
  "content": {
    "symbol": "BTCUSDT",
    "price": 75000.00,
    "timestamp": 1720000000
  },
  "is_test": false
}
```
- `type`：信号类型，"buy" 或 "sell"
- `content.symbol`：交易对（如 "BTCUSDT"）
- `content.price`：价格
- `content.timestamp`：Unix 时间戳（秒）
- `is_test`：是否为测试消息

### 客户端可发送命令
- `test`：请求服务器发送测试数据

## 客户端集成示例（JavaScript）

```javascript
const token = 'your_secure_token_here'; // 替换为您的访问令牌
const socket = new WebSocket('wss://example.com:8080', {
    headers: {
        'Authorization': `Bearer ${token}`
    }
});

socket.addEventListener('open', () => {
    console.log('已连接到 WebSocket 服务器');
});

socket.addEventListener('message', (event) => {
    const data = JSON.parse(event.data);
    console.log('收到信号:', data);
    if (data.type === 'buy') {
        console.log(`买入信号：${data.content.symbol}，价格：${data.content.price}`);
    } else if (data.type === 'sell') {
        console.log(`卖出信号：${data.content.symbol}，价格：${data.content.price}`);
    }
});

socket.addEventListener('close', () => {
    console.log('连接已关闭');
});

socket.addEventListener('error', (event) => {
    console.error('WebSocket 错误:', event);
});

// 发送测试命令
function requestTestData() {
    socket.send('test');
}
```

## 断线重连建议

建议实现自动重连：
- 初始延迟 1 秒，指数退避，最大 30 秒

## Python 客户端示例

```python
import websocket
import json
import threading
import time
from websocket import create_connection

def on_message(ws, message):
    data = json.loads(message)
    print(f"收到信号: {data}")
    if data['type'] == 'buy':
        print(f"买入信号：{data['content']['symbol']}，价格：{data['content']['price']}")
    elif data['type'] == 'sell':
        print(f"卖出信号：{data['content']['symbol']}，价格：{data['content']['price']}")

def on_error(ws, error):
    print(f"WebSocket 错误: {error}")

def on_close(ws, close_status_code, close_msg):
    print("连接已关闭")

def on_open(ws):
    print("WebSocket 连接已建立")

# 创建带认证头的 WebSocket 连接
def create_authenticated_ws(url, token):
    ws = websocket.WebSocketApp(
        url,
        header=[f"Authorization: Bearer {token}"],
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
        on_open=on_open
    )
    return ws

# 使用示例
if __name__ == "__main__":
    token = "your_secure_token_here"  # 替换为您的访问令牌
    ws_url = "wss://example.com:8080"  # 替换为实际的 WebSocket 地址
    
    # 创建并运行 WebSocket 客户端
    ws = create_authenticated_ws(ws_url, token)
    ws.run_forever()

def on_open(ws):
    print("连接已建立")
    def run():
        time.sleep(2)
        ws.send("test")
        print("请求了测试数据")
    threading.Thread(target=run).start()

if __name__ == "__main__":
    ws = websocket.WebSocketApp(
        "ws://example.com:8080",
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )
    ws.run_forever()
