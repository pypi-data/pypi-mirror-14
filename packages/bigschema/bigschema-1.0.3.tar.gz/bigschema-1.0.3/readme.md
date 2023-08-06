### BigSchema

This library is meant as a simple way to generate the big query boilerplate   
given a simple yaml based schema.


#### CLI Tool

The library comes with a simple command line tool that takes a source file,    
an optional destination directory default is ```./schema/``` and an output    
format and transforms the given yaml specifications to BigQuery compliant    
schema in the desired output format.

```bash
$ bigschema --help

Usage: bigschema [OPTIONS] SOURCE [DESTINATION]
Options:
  -f, --output-format [java|json]
                                  Which format to output the data in? Default
                                  is JSON
  -o, --overwrite BOOLEAN         Should we overwrite the data in existing
                                  file? Default is FALSE
  --help                          Show this message and exit.
  
```


#### File Specification

```yaml
spec-mode: "compact" | "verbose"

---------------------------------------------------------------------------------
spec-mode: "verbose"
--------------------

table:
  type: "table"
  fields:
    - name:
      type: "integer" | "float" | "string" | "timestamp" | "boolean" | "bytes" | "record_name"
      mode: "nullable" | "repeated" | "required"

record:
  type: "record"
  fields:
    - name:
      type: "integer" | "float" | "string" | "timestamp" | "boolean" | "bytes" | "record_name"
      mode: "nullable" | "repeated" | "required"


----------------------------------------------------------------------------------
spec-mode: "compact"
--------------------

table:
  type: table
  fields:
    - name_of_column, type_of_column, mode_of_column

record:
  type: record
  fields:
    - name_of_column, type_of_column, mode_of_column
```
