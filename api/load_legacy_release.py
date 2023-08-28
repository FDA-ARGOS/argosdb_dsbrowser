import os,sys
import string
from optparse import OptionParser
import glob
import json
from bson import json_util
import pymongo
from pymongo import MongoClient
import datetime


__version__="1.0"
__status__ = "Dev"



###############################
def main():


    usage = "\n%prog  [options]"
    parser = OptionParser(usage,version="%prog version___")
    parser.add_option("-s","--server",action="store",dest="server",help="dev/tst/beta/prd")
    parser.add_option("-v","--dataversion",action="store",dest="dataversion",help="2.0.2/2.0.3 ...")
        
    (options,args) = parser.parse_args()

    for key in ([options.dataversion, options.server]):
        if not (key):
            parser.print_help()
            sys.exit(0)

    server = options.server
    ver = options.dataversion

    config_obj = json.loads(open("./conf/config.json", "r").read())
    mongo_port = config_obj["dbinfo"]["port"][server]
    host = "mongodb://127.0.0.1:%s" % (mongo_port)

    jsondb_dir = config_obj["data_path"] + "/releases/data/v-%s/jsondb/" % (ver)

    dir_list = os.listdir(jsondb_dir)

    
    db_name = config_obj["dbinfo"]["dbname"]
    db_user, db_pass = config_obj["dbinfo"][db_name]["user"], config_obj["dbinfo"][db_name]["password"]


    try:
        client = pymongo.MongoClient(host,
            username=db_user,
            password=db_pass,
            authSource=db_name,
            authMechanism='SCRAM-SHA-1',
            serverSelectionTimeoutMS=10000
        )
        client.server_info()
        dbh = client[db_name]
        for d in dir_list:
            if d[-2:] != "db":
                continue
            coll = "c_" + d[:-2]
            
            if coll not in ["c_extract", "c_bco", "c_history"]:
                continue

            coll = "%s_v-%s" % (coll, ver)
            result = dbh[coll].delete_many({})
            file_list = glob.glob(jsondb_dir + "/" + d + "/*.json")
            nrecords = 0
            for in_file in file_list:
                doc = json.loads(open(in_file, "r").read())
                if "_id" in doc:
                    doc.pop("_id")
                if "object_id" in doc:
                    bco_id = doc["object_id"].split("/")[-2]
                    doc["object_id"] = "https://biocomputeobject.org/%s/%s" % (bco_id, ver)
                result = dbh[coll].insert_one(doc)     
                nrecords += 1
                if nrecords != 0 and nrecords%1000 == 0:
                    ts = datetime.datetime.now()
                    print (" ... loaded %s documents to %s [%s]" % (nrecords, coll, ts))
            ts = datetime.datetime.now()
            print (" ... loaded %s documents to %s [%s]" % (nrecords, coll, ts))
    except pymongo.errors.ServerSelectionTimeoutError as err:
        print (err)
    except pymongo.errors.OperationFailure as err:
        print (err)



if __name__ == '__main__':
    main()
