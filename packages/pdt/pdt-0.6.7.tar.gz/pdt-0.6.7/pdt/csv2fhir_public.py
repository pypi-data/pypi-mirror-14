#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
# Written by Alan Viars - This software is public domain

import os, sys, string, json, csv, time
from collections import OrderedDict
from datetime import datetime



def newfhir_deactive_stub():
    ps = OrderedDict()
    
    #ProviderJSON stub
    ps["resourceType"] = "Practitioner"
    ps['identifier'] = [
                    {
                      "use": "official",
                      "system": "http://hl7.org/fhir/sid/us-npi",
                      "value": "",
                      "_value": {
                        "fhir_comments": [
                          "   NPI  "
                        ]
                      }
                    }
                  ]
    return ps
    
def new_fhir_practitioner_stub(npi, prefix, first_name, last_name, suffix):
    
    
    text = "%s %s %s %s %s" % (npi, prefix, first_name, last_name, suffix)
    ps = OrderedDict()
    ps["resourceType"] = "Practitioner"
    ps["text"] = { "status": "generated",
                   "div": "<div><p>%s</p></div>" % (text)
                 }
    ps['identifier'] = [
                    {
                      "use": "official",
                      "system": "http://hl7.org/fhir/sid/us-npi",
                      "value": npi,
                      "_value": {
                        "fhir_comments": [
                          "   NPI  "
                        ]
                      }
                    }
                  ]
    ps['name'] = [
                {
                  "family": [
                    last_name
                  ],
                  "given": [
                    first_name
                  ],
                  "suffix": [
                    suffix
                  ],
                  "prefix": [
                    prefix
                  ]
                    
                    
                }
              ]
    ps["address"]= [
            {
              "use": "work",
              "line": [],
              "city": "",
              "district": "",
              "state": "",
              "postalCode": "",
              "country": "USA"
            },
            {
              "use": "mailing",
              "line": [],
              "city": "",
              "district": "",
              "state": "",
              "postalCode": "",
              "country": "USA"
            }
            
            
          ]
    
    
    return ps
    


def new_fhir_organization_stub(npi, organization_name):
    
    text = "NPI %s for %s" % (npi, organization_name)
    os = OrderedDict()
    os["resourceType"] = "Organization"
    os["npi"] = npi
    os["text"] = { "status": "generated",
                   "div": "<div><p>%s</p></div>" % (text)
                 }
    os['identifier'] = [
                    {
                      "use": "official",
                      "system": "http://hl7.org/fhir/sid/us-npi",
                      "value": npi,
                      "_value": {
                        "fhir_comments": [
                          "   NPI  "
                        ]
                      }
                    }
                  ]
    os['name'] = organization_name
    os['telecom'] = [
                    {
                        "system":"phone",
                        "value":"",
                        "use":"practice"
                    },
                    {
                        "system":"fax",
                        "value":"",
                        "use":"practice"
                    },
                    {
                        "system":"phone",
                        "value":"",
                        "use":"business"
                    },
                    {
                        "system":"fax",
                        "value":"",
                        "use":"business"
                    }
                ]
    
    
    os["address"]= [
            {
              "use": "work",
              "line": [],
              "city": "",
              "district": "",
              "state": "",
              "postalCode": "",
              "country": "USA"
            },
            {
              "use": "mailing",
              "line": [],
              "city": "",
              "district": "",
              "state": "",
              "postalCode": "",
              "country": "USA"
            }
            
            
          ]
    
    return os





def publiccsv2fhir(csvfile, output_dir):

    """Return a response_dict with summary of  publiccsv2fhir transaction."""


    process_start_time = time.time()
    
    pdir = 1
    
  
    #make the output dir
    try:
        os.mkdir(output_dir)
    except:
        pass
     
     
    response_dict = OrderedDict()
    fh = open(csvfile, 'rb')
    csvhandle = csv.reader(fh, delimiter=',')
    rowindex = 0
    po_count = 0
    error_list = []   
        
    for row in csvhandle :
        if rowindex==0:
                 
            rowindex += 1    
            column_headers = row
             
            cleaned_headers = []
            for c in column_headers:
                c= c.replace(".", "")
                c= c.replace("(", "")
                c= c.replace(")", "")
                c =c.replace("$", "-")
                c =c.replace(" ", "_")
                cleaned_headers.append(c)
        else:

            #If the records is not redacted (because its inactive)
            
            zip_record = zip(cleaned_headers, row)
            record = dict(zip(cleaned_headers, row))
            
            #get rid of blanks 
            no_blank_zip = []
            for i in zip_record:
                if i[1]:
                    no_blank_zip.append(i)
                        
            #start our object off with a stub.
            
            if row[1]:
                p = new_pjson_stub()
                
                
            if row[1] == "1":
                r =  new_fhir_practitioner_stub(row[0], row[6],  row[6], row[5], row[10])
            
            elif row[1] == "2":
                r =  new_fhir_organization_stub(row[0], row[4])
                

            # Add addresses
            #location ---
            a = OrderedDict()
            a["country_code"]                    = row[33].upper()
            a["address_purpose"]                 = "LOCATION"
            
            if a["country_code"] == "US":
                a["address_type"]                    = "DOM"
                a["address_1"]                       =  row[28].upper()
                a["address_2"]                       =  row[29].upper()
                a["city"]                            =  row[30].upper()
                a["state"]                           =  row[31].upper()
                a["zip"]                             =  row[32].upper()
                                    
                if row[34]:
                    
                    a["us_telephone_number"]         =  "%s-%s-%s" % (row[34][0:3], row[34][3:6], row[34][6:12])
                
                if  row[35]:    
                    a["us_fax_number"]               =  "%s-%s-%s" % (row[35][0:3], row[35][3:6], row[35][6:12])

                
            else:
                a["address_type"]                    = "FGN"
                a["address_1"]                       =  row[28].upper()
                a["address_2"]                       =  row[29].upper()
                a["city"]                            =  row[30].upper()
                a["foreign_state"]                   =  row[31].upper()
                a["foreign_postal"]                  =  row[32].upper()                   
                a["foreign_telephone_number"]        =  row[34].upper()
                a["foreign_fax_number"]              =  row[35].upper()


            r['address'].append(a)
            
            #Mailing address ---
            a = OrderedDict()
            a["country_code"]                    = row[25].upper()
            a["address_purpose"]                 = "MAILING"
            
            if a["country_code"] == "US":
                a["address_type"]                    = "DOM"
                a["address_1"]                       =  row[20].upper()
                a["address_2"]                       =  row[21].upper()
                a["city"]                            =  row[22].upper()
                a["state"]                           =  row[23].upper()
                a["zip"]                             =  row[24].upper()
                
                if row[26]:
                    a["us_telephone_number"] =  "%s-%s-%s" % (row[26][0:3], row[26][3:6], row[26][6:12])
                
                if row[27]:
                    a["us_fax_number"]       =  "%s-%s-%s" % (row[27][0:3], row[27][3:6], row[27][6:12])
                
            else:
                a["address_type"]                    = "FGN"
                a["address_1"]                       =  row[20].upper()
                a["address_2"]                       =  row[21].upper()
                a["city"]                            =  row[22].upper()
                a["foreign_state"]                   =  row[23].upper()
                a["foreign_postal"]                  =  row[24].upper()
                a["foreign_telephone_number"]        =  row[26].upper()
                a["foreign_fax_number"]              =  row[27].upper()


            r['address'].append(a)
                
                      
            fn = "%s.json" % (row["0"])
            
            subdir = os.path.join(output_dir, str(row["0"])[0:4])
            
            try:
                os.mkdir(subdir)
            except:
                pass
                   
                
            fp = os.path.join(subdir, fn)
            ofile =  open(fp, 'w')
            ofile.writelines(json.dumps(p, indent =4))
            ofile.close()
            po_count += 1
            
            if po_count % 1000 == 0:
               pdir += 1
               out  = "%s files created. Total time is %s seconds." % (po_count ,(time.time() - process_start_time) )
               print out   
               
        
            rowindex += 1


        if error_list:
                response_dict['num_files_created']=rowindex-1
                response_dict['num_file_errors']=len(error_list)
                response_dict['errors']=error_list
                response_dict['code']=400
                response_dict['message']="Completed with errors."
        else:

                response_dict['num_files_created']=rowindex -1
                response_dict['num_csv_rows']=rowindex -1
                response_dict['code']=200
                response_dict['message']="Completed without errors."

    return response_dict

if __name__ == "__main__":

    
    if len(sys.argv)!=3:
        print "Usage:"
        print "csv2fhir-public.py [CSVFILE] [OUTPUT_DIRECTORY]"
        sys.exit(1)

    csv_file   = sys.argv[1]
    output_dir = sys.argv[2]

    result = publiccsv2fhir(csv_file, output_dir)
    
    #output the JSON transaction summary
    print json.dumps(result, indent =4)
