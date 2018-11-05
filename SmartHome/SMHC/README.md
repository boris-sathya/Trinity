# Smart Home Controller

## APIs

### View Registered Devices

**Request**

`GET /devices`

**Response**

- 200: ok

```json
[
	{
		"id": "1",
		"device": "192.168.1.55",
		"power": "40",
		"name": "Floor Lamp",
		"type": "light",
		"controller": "192.168.1.25",
		"location": "bedroom"
	},
	{
		"id": "2",
		"device": "192.168.1.56",
		"power": "1000",
		"name": "Convection Heater",
		"type": "heater",
		"controller": "192.168.1.25",
		"location": "bedroom"
	}
]
```

### Register New Device

**Request**

`POST /devices`

**Parameters**

- `"id":int`
- `"device":string`
- `"power":int`
- `"name":string`
- `"type":string`
- `"controller":string`
- `"location":string`

**Response**

- 200: ok

### Fetch a specific device
**Request**

`GET /device/<id>`

**Response**

- 404: Device not found
- 200: ok

```json
{
	"id": "2",
	"device": "192.168.1.56",
	"power": "1000",
	"name": "Convection Heater",
	"type": "heater",
	"controller": "192.168.1.25",
	"location": "bedroom"
}
```

### Delete a device
**Request**

`DELETE /device/<id>`

**Response**

- 404: Device not found
- 200: ok
