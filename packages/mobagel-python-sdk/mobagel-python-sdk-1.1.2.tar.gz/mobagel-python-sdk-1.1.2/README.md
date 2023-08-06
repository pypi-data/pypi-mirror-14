# mobagel-python-sdk

## Introduce

MoBagel is a real-time cloud analytics platform that helps IoT companies monitor and analyze hardware usage, speed up research and development, forecast sales and marketing strategies, and proactively engage with customers to prevent product returns. As a result, companies can also save up to millions in cost reductions.

## Installation
Before run mobagel-python-sdk, you need to install [pip](https://pip.pypa.io/en/stable/) first.
### pip (Mac OS X)
```shell
	$ sudo easy_install pip
```
### pip (Ubuntu 14.04)
```shell
	$ sudo apt-get install python-pip python-dev build-essential 
	$ sudo pip install --upgrade pip 
```
### mobagel-python-sdk
```shell
	$ sudo pip install mobagel-python-sdk
```

## Getting Started

#### - Creating an account

If you do not have an account, please create an account [here](https://app.mobagel.com/signup). After you create an account, you will be directed to the dashboard.

#### - Creating a new product
To use MoBagel, you first have to create a **product**, which is essentially a group of same **devices**. You can create new products in the dashboard.

For example:

[Product Name] iBulb
[Product Brief] Smart light bulb
[Product Description] Wi-Fi connected light bulb with motion sensors and temperature sensors.
After you create a **product**, the system will generate a **product_key**, which will be used to create  **devices** later on.

#### - Register your first device
Once you generated a product_key from the dashboard, you can use the product_key and registerDevice function to register a device in your application.

	# Import package
	import pybagel
	import json

	product_key = "YOUR_PRODUCT_KEY"
	# Initialize a Client Instance by product_key
	client = pybagel.Client(product_key=product_key)
	
	# Register a device_key by client
	code, content = client.registerDevice()
	response = json.loads(content.decode('utf-8'))
	device_key = response["data"]["attributes"]["key"];
	# Save device_key


#### - Connecting custom properties or events
In your device application, you will need to prepare your report before sending it to MoBagel.

* Determining different states of your devices to send along with your report

		# Example states

		"state": "normal"
		"state": "error"

* Adding custom properties or events with a key beginning with c_

		# Example custom properties or events

		"c_temperature": 30
		"c_event": "turned_on"
* Deciding when to send reports (time, frequency, events)


#### - Sending first report
Once you connect the sensor properties, you can generate a report with the sendReport function.

    # Sample report
	device_key = "YOUR_DEVICE_KEY"
	report_content = {
	            "state": "Put your state here!",
	            "c_customization" : "python_sdk_test",
	            "c_develop_zone" : "PythonSDK"
	        }
	
	# SendReport
	code, content = client.sendReport(
	    device_key=device_key,
	    content=report_content
	)
	client.sendReport(device_key, content)

## Full sample
You can see example codes at github: /mobagel-python-sdk/example/
[click me](https://github.com/MoBagel/mobagel-python-sdk/tree/master/example)


	__author__ = "MoBagel Inc."
	
	import json
	import pybagel
	from pprint import pprint
	
	print "\nThis is MoBagel Python SDK sample, you can learn how to `register device` and `report state` in this sample code\n"
	
	product_key = "1111111111222222222233333333334444444444555555555566666666667777"
	# Initialize a Client Instance by product_key
	client = pybagel.Client(product_key=product_key)
	
	print "Register device..."
	# register a device_key by client
	code, content = client.registerDevice()
	response = json.loads(content.decode('utf-8'))
	print "Data response: "
	pprint(response)
	
	print "\n========================================================\n"
	
	print "Send report..."
	
	device_key = response["data"]["attributes"]["key"];
	content = {
	            "state": "Put your state here!",
	            "c_customization" : "python_sdk_test",
	            "c_develop_zone" : "PythonSDK"
	        }
	
	# SendReport
	code, content = client.sendReport(
	    device_key=device_key,
	    content=content
	    )
	# return report_id and report_timestamp
	response = json.loads(content.decode('utf-8'))
	print "Data response: "
	pprint(response)




## More
You can visit our home page and get more information.
[https://mobagel.com](https://mobagel.com)

## Author

MoBagel, us@mobagel.com

## License

MoBagel Software Development Kit (SDK) License Agreement


Subject to the terms of this License Agreement, you are hereby granted a worldwide, royalty-free, non-assignable, non-exclusive, and non-sublicensable license to use, copy, modify, and distribute this software in source code or binary form to use the SDK solely to develop applications to connect with MoBagel’s platform.

MoBagel owns all legal right, title and interest in and to the SDK. MoBagel reserves all rights not expressly granted to you. 

The form and nature of the SDK that MoBagel provides may change without prior notice to you. This SDK is provided “as is”, without warranty of any kind, express or limited. MoBagel may stop (permanently or temporarily) providing the SDK to users at MoBagel's sole discretion without prior notice.

You are not granted the right to use MoBagel’s trademarks, logos, domain names, or other distinctive brand features. 
