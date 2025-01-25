import spacy
import json
import argparse
import pymupdf as pdf
from os import listdir
from helpers.iocs import Iocs
from helpers.ttps import Ttps
from helpers.malware_detect import Malware
from helpers.threat_actors import ThreatActors
from helpers.targeted_entities import TargetedEntities

nlp = spacy.load("en_core_web_sm")

def read_file(filename):
    if ".txt" in filename:
        with open(filename, 'r') as file:
            return file.read()
    elif ".pdf" in filename:
        file = pdf.open(filename)
        text = ""
        for page in file:
            text += str(page.get_text())
        return text

def display(filename, data, out_dir, show):
    if not out_dir and show:
        print(filename)
    if out_dir:
        with open(f"{out_dir}/{filename.split('.')[0]}.json", 'w') as file:
            file.write(data)
    else:
        print(data)

def start(report_text):
    iocs = Iocs(report_text)
    ttps = Ttps(report_text, nlp)
    threat_actors = ThreatActors(report_text, nlp)
    malware = Malware(report_text)
    targeted_entities = TargetedEntities(report_text, nlp)

    data = {
        "IoCs": iocs.get_info(),
        "TTPs": ttps.get_info(),
        "Threat Actor(s)": threat_actors.get_info(),
        "Malware": malware.get_info(),
        "Targeted Entities": targeted_entities.get_info(),
    }
    return json.dumps(data, indent=4)
  
if __name__=="__main__":
    parser = argparse.ArgumentParser(
        prog="Solution",
        description="Extracts Key Threat Intelligence Data From Given File, including Indicators of Compromise, TTTps, Malware Information, Threat Actors and Targeted Entities"
    )
    parser.add_argument("-f", "--file", help = "Filename to process, can be .pdf or .txt only")
    parser.add_argument("-d", "--dir", help = "Directory to search files in, will not search recursively")
    parser.add_argument("-o", "--out", help = "Directory to store output .json file, output filename is same as input filename")
    parser.add_argument("-s", "--show", help = "Prints filename to stdout", action="store_true")
    args = parser.parse_args()
    arg = vars(args)

    if not arg['dir'] and not arg['file']:
        parser.parse_args(['-h'])
    if arg["dir"]:
        files = listdir(arg["dir"])
        for file in files:
            display(file, start(read_file(f"{arg['dir']}/{file}")), arg["out"], arg["show"])
    if arg["file"]:
        display(arg["file"], start(read_file(arg["file"])), arg["out"], arg["show"])
