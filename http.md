# 交易系统 API 文档

## 目录
- [认证](#认证)
- [响应格式](#响应格式)
- [接口列表](#接口列表)
  - [GET /pnl_summary](#get-pnl_summary)
  - [GET /positions](#get-positions)
  - [GET /trades](#get-trades)
  - [GET /signals](#get-signals)

## 认证

所有 API 请求都需要在 `Authorization` 头中携带 Bearer Token 进行身份验证。

```http
Authorization: Bearer {token}
```

### 错误响应（未授权）
```json
{
  "code": 401,
  "message": "Invalid or expired token",
  "data": []
}
```

## 响应格式

### 成功响应
```json
{
  "code": 200,
  "message": "success",
  "data": []
}
```

### 错误响应
```json
{
  "code": 500,
  "message": "error message",
  "data": []
}
```

## 接口列表

### GET /pnl_summary

获取盈亏汇总数据。

#### 查询参数
| 参数        | 类型     | 必填    | 默认值 | 说明                           |
|-------------|----------|---------|--------|--------------------------------|
| strategy    | string   | 否      | -      | 按策略代码过滤                 |
| start_time  | string   | 否      | -      | 开始时间，格式为 YYYY-MM-DD    |
| end_time    | string   | 否      | -      | 结束时间，格式为 YYYY-MM-DD    |
| offset      | integer  | 否      | 0      | 跳过的记录数                   |
| limit       | integer  | 否      | 20     | 返回的最大记录数（时间范围查询最大1000，否则最大100） |

#### 说明
- 未指定 `strategy` 时，返回每个策略的最新一条记录（忽略 limit 参数）
- 未指定 `start_time` 和 `end_time` 时，返回最近的 20 条记录
- 最大时间跨度为 3 个月
- 使用时间范围查询时，limit 最大为 1000 条

#### 请求示例
```http
GET /pnl_summary?strategy=b01&offset=0&limit=20&start_time=2025-06-04&end_time=2025-07-04
```

#### 响应示例
```json
{
  "code": 200,
  "message": "success",
  "data": [
    {
      "id": 1,
      "start_time": "2025-07-04T16:04:41Z",
      "end_time": "2025-07-04T16:19:00Z",
      "total_profit_loss": "5.84340530",
      "total_trades": 62,
      "winning_trades": 37,
      "losing_trades": 25,
      "strategy": "b01",
      "created_at": "2025-07-04T16:19:00Z"
    }
  ]
}
```

### GET /positions

获取当前持仓信息。

#### 查询参数
| 参数      | 类型     | 必填 | 默认值 | 说明             |
|-----------|----------|------|--------|------------------|
| strategy  | string   | 是   | -      | 按策略代码过滤   |
| offset    | integer  | 否   | 0      | 跳过的记录数     |
| limit     | integer  | 否   | 20     | 返回的最大记录数（最大100） |

#### 请求示例
```http
GET /positions?strategy=b01&offset=0&limit=20
```

#### 响应示例
```json
{
  "code": 200,
  "message": "success",
  "data": [
    {
      "id": 5,
      "symbol": "BTCUSDT",
      "entry_price": "10417.32031250",
      "quantity": "0.01000000",
      "entry_time": "2025-07-04T16:57:14Z",
      "last_update": "2025-07-04T16:57:14Z",
      "unrealized_pnl": "0.00000000",
      "strategy": "b01"
    }
  ]
}
```

### GET /trades

获取交易历史。

#### 查询参数
| 参数      | 类型     | 必填 | 默认值 | 说明           |
|-----------|----------|------|--------|----------------|
| strategy  | string   | 是   | -      | 按策略代码过滤 |
| offset    | integer  | 否   | 0      | 跳过的记录数   |
| limit     | integer  | 否   | 20     | 返回的最大记录数（最大100） |

#### 请求示例
```http
GET /trades?strategy=b01&offset=0&limit=20
```

#### 响应示例
```json
{
  "code": 200,
  "message": "success",
  "data": [
    {
      "id": 591,
      "signal_id": 596,
      "trade_type": "BUY",
      "symbol": "BTCUSDT",
      "price": "10417.32000000",
      "quantity": "0.01000000",
      "fee": "0.00000000",
      "timestamp": "2025-07-04T16:57:14Z",
      "profit_loss": null,
      "strategy": "b01"
    },
    {
      "id": 590,
      "signal_id": 593,
      "trade_type": "SELL",
      "symbol": "BTCUSDT",
      "price": "10970.47000000",
      "quantity": "0.01000000",
      "fee": "0.00000000",
      "timestamp": "2025-07-04T16:56:59Z",
      "profit_loss": "2.33147500",
      "strategy": "b01"
    }
  ]
}
```

### GET /signals

获取交易信号。

#### 查询参数
| 参数      | 类型     | 必填 | 默认值 | 说明           |
|-----------|----------|------|--------|----------------|
| strategy  | string   | 是   | -      | 按策略代码过滤 |
| offset    | integer  | 否   | 0      | 跳过的记录数   |
| limit     | integer  | 否   | 20     | 返回的最大记录数（最大100） |

#### 请求示例
```http
GET /signals?strategy=b01&offset=0&limit=20
```

#### 响应示例
```json
{
  "code": 200,
  "message": "success",
  "data": [
    {
      "id": 595,
      "symbol": "BTCUSDT",
      "signal_type": "sell",
      "price": "10433.53000000",
      "quantity": "0.01000000",
      "timestamp": "2025-07-04T16:57:09Z",
      "strategy": "b01",
      "parameters": "{}",
      "executed": false,
      "notes": null
    },
    {
      "id": 594,
      "symbol": "BTCUSDT",
      "signal_type": "sell",
      "price": "10111.04000000",
      "quantity": "0.01000000",
      "timestamp": "2025-07-04T16:57:04Z",
      "strategy": "b01",
      "parameters": "{}",
      "executed": false,
      "notes": null
    }
  ]
}
```
