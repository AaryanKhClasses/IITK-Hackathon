# PS1: Uncovering Threat Intelligence from Cybersecurity Reports

## **Code Implementations:**
The main python script is found in the root directory of the project.
The project is structured into different helper classes found in the `~/helpers` directory.
These helper classes have functions to get the information of the IoCs, TTPs, Threat Actor(s), Malware Information, and Targeted Entities.

### **The Main Script File:**
The main python file `~/solution.py` is ran to get the output.
The library spaCy is used to create a Natural Language Processor (NLP), and it loads a pre-defined NLP of `en_core_web_sm`, which is used throughout the program.

The main script file includes the classes of all the other helper files and provides the files the NLP initiated, to get back the desired dictionary required.
It is then printed out to the console as an output.

### Indicators of Compromise (IoCs):
The python script gets the IoCs in the report text/pdf using a ReGeX query specifically from file hashes, email addresses, domain names, and IP addresses.

The output of the following is in the format of:
```json
{
	"IOCs": {
		"IP Addresses": [],
		"Domains": [],
		"File Hashes": [],
		"Email Addresses": []
	}
}
```

### Tactics, Techniques, Protocols (TTPs):
These are identified in accordance with the **Mitre ATT&CK Framework**.
The dataset of the tactics and techniques are gathered from a JSON file directly within the script
```
https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json
```
The NLP initiated in the main script is provided to this file and then the matched tactics and techniques are sent as the output, which is in the form of:
```json
{
	"TTPs": {
		"Tactics": [],
		"Techniques": []
	}
}
```

### Threat Actor(s):
Here a simple NLP usage is done, where terms related to organizations, geolocations, etc. are found and are sent as output, which is in the form of:
```json
{
	"Threat Actor(s)": []
}
```

### Targeted Entities:
Similar to Threat Anchor(s), this also searches for organizations and geolocations, not included in the threat actor list, and this specifically looks for sectors like organizations, industries, etc.
```json
{
	"Targeted Entities": []
}
```

### Malware:
This section requires a VirusTotal API Key to be provided in order for the script to search for malware on the web. This works by gathering the file hashes in the document and then using the VirusTotal API, it gets the required information:
```json
{
	"Malware": [
		[{
			"name": "",
			"sha1": "",
			"sha256": "",
			"md5": "",
			"ssdeep": "",
			"vhash": "",
			"tlsh": "",
			"tags": [""]
		}]
	]
}
```


## **Documentation:**

### Prerequisites:
1) **Python:** As this is a python script, you would require a python instance available on your device. [Click Here to Download Python]([(https://www.python.org/downloads/))
2) **VirusTotal API Key:** Go to [The VirusTotal Website](https://www.virustotal.com/gui/home/upload) and create an account. Now, by clicking your user profile (in the Navbar), navigate to the API Key section. Just copy and paste the API Key into the .env.example file, and then rename the file to .env

> [!WARNING]
> The VirusTotal API Key only allows 4 queries/min and 500 queries/day.

### Dependencies:
**Python Libraries:** This project uses some python scripts, which can be easily installed as:
```bat
   $ pip install spacy re requests os python-dotenv json argparse pymupdf
```
- **spaCy:** It is the library used for the Natural Language Processing (NLP) in the program.
- **re:** It is a ReGeX library, used for detecting the Email IDs, File Hashes, etc.
- **requests:** It is the library used to fetch (get) request through the VirusTotal API.
- **os:** It is the library used for directory related purposes, like getting the report text file or the pdf file for the scan.
- **python-dotenv:** The `VIRUSTOTAL_API_KEY` is stored in a .env file for it to be not compromised, and to get the API key in the program, this library is used.
- **json:** It is the library used to get the final output.
- **argparse:** It is used for the CLI operations as mentioned below.
- **pymupdf:** It is used to convert the pdf files into the required format for them to be `report_text`.

**Getting the NLP Model:** To get the spaCy NLP model for our program, run the following:
```bat
$ python -m spacy download en_core_web_sm
```

### Logic:
The python script initiates an NLP and takes the `report_text` in the form of a file as mentioned below, then the `report_text` is passed onto the various helper classes to get information about the IOCs, TTPs, Malwares, Threat Actor(s), and Targeted Entities, as mentioned above.

All the data is passed back onto the main script and the output is result is displayed onto the terminal (or in the specified output directory.)

## **Additional Features:**
The python script is not to be run directly, if you execute the command:
```bat
$ python3 solution.py
```
Then it will show a help dialog, saying that certain flags are supposed to be used with it.
1) **-f flag:** You need to specify a file (.txt or .pdf) in which your `report_text` is stored in, which will be processed by the NLP and ReGeX to give the output.
```bat
$ python3 solution.py -f "file_path"
$ python3 solution.py --file "file_path"
```

2) **-d flag:** If you have multiple files stored in a directory, the program will run through all the files (.txt or .pdf) in the directory and give outputs for each one.
```bat
$ python3 solution.py -d "dir_path"
$ python3 solution.py --dir "dir_path"
```

3) **-o flag:** If you want the JSON output to be a file, pass a directory onto the flag and the JSON file (name same as that of input file) will be stored in that directory.
```bat
$ python3 solution.py <file/dir input> -o "dir_path"
$ python3 solution.py <file/dir input> --out "dir_path"
```

