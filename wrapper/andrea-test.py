import time
import multichain
import logging

#logging.basicConfig(filename='myapp.log', level=logging.INFO)
logging.basicConfig(level=logging.INFO)

class getting_started:
    logger = logging.getLogger(__name__)
    rpcuser = "multichainrpc"
    rpcpasswd = "AjAoAutxA8yoRZHHn9nPsQo6346oMsATzZrhrwZzBbu8"
    rpchost = "127.0.0.1"
    rpcport = "6478"
    chainname = "chain1"
    api = multichain.api_call(rpcuser, rpcpasswd, rpchost, rpcport, chainname)

    def create_stream(self, name: str, restrictions = {"restrict": "write"}) -> str:
        """
        Possibili valori per restrict: "offchain,onchain,write,read"}
        Altra chiave per restrictions: "salted": true (default per restrict read per esempio)
        """
        self.logger.debug(f"Creating strem '{name}' with the following restrictions: '{restrictions['restrict']}'")
        retval = self.api.create("stream", name, restrictions)
        self.logger.debug(f"Strem '{name}' created in txid {retval}")
        return retval
    
    def listpermissions(self, permissions = "*", addresses = "*", verbose = False) -> dict:
        """
        Retval di esempio:
        [{'address': '1TMxmPGSbTMN7Jmnh5HXKNDUBWR8YG2q2cFK1y', 'for': {'type': 'stream', 'name': 'stream1', 'streamref': '60-266-24252'}, 'type': 'admin', 'startblock': 0, 'endblock': 4294967295}, {'address': '1TMxmPGSbTMN7Jmnh5HXKNDUBWR8YG2q2cFK1y', 'for': {'type': 'stream', 'name': 'stream1', 'streamref': '60-266-24252'}, 'type': 'activate', 'startblock': 0, 'endblock': 4294967295}, {'address': '1TMxmPGSbTMN7Jmnh5HXKNDUBWR8YG2q2cFK1y', 'for': {'type': 'stream', 'name': 'stream1', 'streamref': '60-266-24252'}, 'type': 'write', 'startblock': 0, 'endblock': 4294967295}, {'address': '1TMxmPGSbTMN7Jmnh5HXKNDUBWR8YG2q2cFK1y', 'for': {'type': 'stream', 'name': 'stream1', 'streamref': '60-266-24252'}, 'type': 'read', 'startblock': 0, 'endblock': 4294967295}]
        """
        self.logger.debug(f"Getting permissions for {permissions}")
        retval = self.api.listpermissions(permissions, addresses, verbose)
        return retval 
    
    def gettransaction(self, txid: str, include_watchonly = False) -> dict:
        self.logger.debug(f"Getting Information about transaction id: {txid}")
        retval = self.api.gettransaction(txid, include_watchonly)
        self.logger.debug(f"Retrieved information for transaction '{txid}': {retval}")
        return retval

    def getrawtransaction(self, txid: str, verbose = False) -> dict:
        self.logger.debug(f"Getting Information about transaction id: '{txid}'")
        retval = self.api.getrawtransaction(txid, verbose)
        self.logger.debug(f"Retrieved information for transaction '{txid}': {retval}")
        return retval

    def decoderawtransaction(self, txhex: str) -> dict:
        self.logger.debug(f"Returns a JSON object describing the serialized transaction in tx-hex for {txhex}")
        retval = self.api.getrawtransaction(txhex)
        return retval

    def publish(self, stream: str, key: str, data: dict) -> str:
        self.logger.debug(f"publishing on {key} in {stream}")
        retval = self.api.publish(stream, key, {"json":data})
        self.logger.debug(f"publishing on {key} in {stream} initializated")
        return retval

    def check_transaction_complete(self, txid: str) -> bool:
        tx = self.gettransaction(txid, False)
        return tx['confirmations'] > 0

    def wait_for_transacioon_to_complete(self, txid: str, timeout = 120) -> bool:
        """
        returns false if timeout is reached, true if transaction is completed
        """
        completed = False
        while (not completed) and (timeout > 0):
            completed = self.check_transaction_complete(txid)
            time.sleep(2)
            timeout -= 2
        return completed

    def listtransactions(self, account: str | None = None, count = 10, start = 0, include_watchonly = True) -> dict:
        self.logger.debug(f"looking for {count} transactions starting at {start}, {"not " if not include_watchonly else ""} including watchonly {f", for account \"{account}\"" if account is not None else "" }")
        retval = None
        if account is not None:
            retval = self.api.listtransactions(account, count, start, include_watchonly)
        else:
            retval = self.api.listtransactions("", count, start, include_watchonly)
        return retval

gs = getting_started()
#print(f"Creating stream 'stream1' with write restriction: {gs.create_stream('stream1', {"restrict": "write"})}")
#### Attendere qualche secondo per il termine della Transazione, non riportata asincrona, check stato della TxID?
#print(f"Permissions list for stream1: {gs.listpermissions('stream1.*')}")
#print(f"Transaction: {gs.gettransaction('945c4aaacb1fee05fa3f2105f4da2c165fba14dca615bfde58344326b1e8f84a')}")
#print(f"Transaction JSON: {gs.gettransaction('945c4aaacb1fee05fa3f2105f4da2c165fba14dca615bfde58344326b1e8f84a', True)}")
#print(f"publish {gs.publish("stream1", "key1", {"name":"John Doe", "city":"London"})}")

"""
txid = gs.publish("stream1", "toyota-corolla-cross-my23-quater", {
    "_links": {
        "self": {
            "href": "https://product-ro.toyota-europe.com/TMI/models/0274AD1E-E249-42EA-9A18-0CCE782F7956/localConfigurations?localModelCode=MXGH12L-KHXEHW-42-202303&includeTechSpecs=True&includeEmbeddedData=True&includeEndUserEquipmentIds=False&includeColours=True&includeVomPrices=False",
            "_ids": [
                "0A281777-A8E4-44AB-B0B6-8D6D4C1275AF"
            ]
        },
        "model": {
            "_id": "0274AD1E-E249-42EA-9A18-0CCE782F7956",
            "href": "https://product-ro.toyota-europe.com/TMI/models/0274AD1E-E249-42EA-9A18-0CCE782F7956"
        }
    },
    "_embedded": {
        "localConfigurations": [
            {
                "_id": "0A281777-A8E4-44AB-B0B6-8D6D4C1275AF",
                "organisation": "TMI",
                "description": "LOUNGE STYLE PACK",
                "comment": "",
                "localModelCode": "MXGH12L-KHXEHW-42-202303",
                "toCode": None,
                "version": 1,
                "base": False,
                "baseConfiguration": {
                    "_id": "DC51C69F-0642-4351-B378-9B7CB13A26BA"
                },
                "fleet": False,
                "bestseller": False,
                "bestsellerA": False,
                "bestsellerB": False,
                "showroom": False,
                "showroomLaunch": False,
                "demo": False,
                "demoLaunch": False,
                "duplicateOfLMC": None,
                "reservable": True,
                "donor": False,
                "specialOrder": False,
                "vehicleType": "PC",
                "vehicleTypeDescription": "Sports Utility Vehicles",
                "productionFrom": "202303",
                "productionTo": "202309",
                "endOfProductionDate": None,
                "lifeCycles": [
                    {
                        "_id": "87E0E4FE-2C93-4BA8-BA1E-21A94CFE0B0D",
                        "description": "Published as current lineup",
                        "type": "TOSHIKO",
                        "typeDescription": "Toshiko",
                        "generalCode": "PublishedAsCurrentLineup",
                        "validFrom": "2023-01-31",
                        "previousLifeCycle": {
                            "_id": "A98CA90D-B54F-4C2B-AED9-BEC96DA696C5"
                        }
                    },
                    {
                        "_id": "A98CA90D-B54F-4C2B-AED9-BEC96DA696C5",
                        "description": "Draft",
                        "type": "TOSHIKO",
                        "typeDescription": "Toshiko",
                        "generalCode": "Draft",
                        "validFrom": "2023-01-13",
                        "previousLifeCycle": None
                    },
                    {
                        "_id": "86C083E6-87CA-4D86-AFB6-80263F39B69B",
                        "description": "Published as previous lineup",
                        "type": "TOSHIKO",
                        "typeDescription": "Toshiko",
                        "generalCode": "PublishedAsPreviousLineup",
                        "validFrom": "2024-01-02",
                        "previousLifeCycle": {
                            "_id": "87E0E4FE-2C93-4BA8-BA1E-21A94CFE0B0D"
                        }
                    },
                    {
                        "_id": "71B77EF5-46BB-46A0-A7CC-04B21FF31CD1",
                        "description": "Draft",
                        "type": "CARDB SYSTEM",
                        "typeDescription": "CarDB System",
                        "generalCode": "Draft",
                        "validFrom": "2023-01-13",
                        "previousLifeCycle": None
                    },
                    {
                        "_id": "84DFBCAE-307C-48D1-A8A9-52D51B732FE1",
                        "description": "Available",
                        "type": "CARDB SYSTEM",
                        "typeDescription": "CarDB System",
                        "generalCode": "Available",
                        "validFrom": "2023-01-17",
                        "previousLifeCycle": {
                            "_id": "71B77EF5-46BB-46A0-A7CC-04B21FF31CD1"
                        }
                    },
                    {
                        "_id": "B35D3761-4BF2-486D-9F1C-90B8CFD04A3D",
                        "description": "New",
                        "type": "PRODUCT",
                        "typeDescription": "Product",
                        "generalCode": "Setup",
                        "validFrom": "2023-01-13",
                        "previousLifeCycle": None
                    }
                ],
                "languages": {
                    "translations": [
                        "it-IT"
                    ]
                },
                "translations": {
                    "it-IT": {
                        "_id": "0FCCBF0C-8AC5-410C-8A1F-3C1D8DBD86B1",
                        "country": "IT",
                        "language": "it",
                        "order": 9,
                        "shortDescription": "2.0 HV FWD LOUNGE STYLE PACK",
                        "longDescription": "COROLLA CROSS 2.0 HV FWD LOUNGE STYLE PACK",
                        "marketingComment": None,
                        "highlight": False
                    }
                },
                "categoryPrices": [
                    {
                        "countryCode": "IT",
                        "categories": [
                            {
                                "category": "DEFAULT",
                                "localConfigurationPrices": [
                                    {
                                        "validFrom": "2023-01-20 00:00:00.0",
                                        "validTo": "2023-12-31 00:00:00.0",
                                        "prices": [
                                            {
                                                "type": "RSP NO VAT",
                                                "amount": 33799.180328,
                                                "currency": "EUR"
                                            },
                                            {
                                                "type": "RSP VAT",
                                                "amount": 42300,
                                                "currency": "EUR"
                                            }
                                        ]
                                    }
                                ],
                                "optionPrices": [
                                    {
                                        "optionId": "CC17286E-7A18-4CB5-9DE3-98EA769DB93D",
                                        "type": "LOCAL_PACK",
                                        "prices": [
                                            {
                                                "validFrom": "2023-01-20 00:00:00.0",
                                                "validTo": "2023-12-31 00:00:00.0",
                                                "prices": [
                                                    {
                                                        "type": "RSP NO VAT",
                                                        "amount": 1229.508197,
                                                        "currency": "EUR"
                                                    },
                                                    {
                                                        "type": "RSP VAT",
                                                        "amount": 1500,
                                                        "currency": "EUR"
                                                    }
                                                ]
                                            }
                                        ],
                                        "_links": {
                                            "self": {
                                                "_id": "CC17286E-7A18-4CB5-9DE3-98EA769DB93D",
                                                "href": "https://product-ro.toyota-europe.com/TMI/models/0274AD1E-E249-42EA-9A18-0CCE782F7956/packs/CC17286E-7A18-4CB5-9DE3-98EA769DB93D"
                                            }
                                        }
                                    }
                                ],
                                "colourPrices": [
                                    {
                                        "colourId": "7F962180-9FEB-41D1-81BD-1579CA23EB54",
                                        "prices": [
                                            {
                                                "validFrom": "2023-01-20 00:00:00.0",
                                                "validTo": "2023-12-31 00:00:00.0",
                                                "prices": [
                                                    {
                                                        "type": "RSP NO VAT",
                                                        "amount": 778.688525,
                                                        "currency": "EUR"
                                                    },
                                                    {
                                                        "type": "RSP VAT",
                                                        "amount": 950,
                                                        "currency": "EUR"
                                                    }
                                                ]
                                            }
                                        ],
                                        "_links": {
                                            "self": {
                                                "_id": "7F962180-9FEB-41D1-81BD-1579CA23EB54",
                                                "href": "https://product-ro.toyota-europe.com/TMI/models/0274AD1E-E249-42EA-9A18-0CCE782F7956/colours/7F962180-9FEB-41D1-81BD-1579CA23EB54"
                                            }
                                        }
                                    },
                                    {
                                        "colourId": "ACE0DCB9-D6E9-4ED9-B6D5-E101788F9398",
                                        "prices": [
                                            {
                                                "validFrom": "2023-01-20 00:00:00.0",
                                                "validTo": "2023-12-31 00:00:00.0",
                                                "prices": [
                                                    {
                                                        "type": "RSP NO VAT",
                                                        "amount": 778.688525,
                                                        "currency": "EUR"
                                                    },
                                                    {
                                                        "type": "RSP VAT",
                                                        "amount": 950,
                                                        "currency": "EUR"
                                                    }
                                                ]
                                            }
                                        ],
                                        "_links": {
                                            "self": {
                                                "_id": "ACE0DCB9-D6E9-4ED9-B6D5-E101788F9398",
                                                "href": "https://product-ro.toyota-europe.com/TMI/models/0274AD1E-E249-42EA-9A18-0CCE782F7956/colours/ACE0DCB9-D6E9-4ED9-B6D5-E101788F9398"
                                            }
                                        }
                                    }
                                ],
                                "otherCostElements": []
                            }
                        ]
                    }
                ],
                "vppmCodes": [],
                "groupDescription": None,
                "groupTCode": None,
                "groupExtendedTo": None,
                "techSpecs": [
                    {
                        "_id": "6D69D1DB-C948-4A8F-805B-4261C5F32FB3",
                        "code": "STEERING",
                        "description": "Steering",
                        "typeCode": "STEE_BLANK",
                        "typeDescription": "",
                        "name": "Turns (lock to lock)",
                        "unitOfMeasure": "",
                        "values": [
                            {
                                "_id": "9A874B6C-8A5B-40B3-B53A-0ABE46FF6C9D",
                                "value": "2.76",
                                "validFrom": "2023-03-01",
                                "validTo": "2999-12-01",
                                "final": None,
                                "languages": {},
                                "translations": {}
                            }
                        ],
                        "languages": {
                            "types": [
                                "it-IT"
                            ]
                        },
                        "translations": {},
                        "unitOfMeasureTranslations": {},
                        "types": {
                            "it-IT": {
                                "_id": "A1DF6115-09EA-4431-9B25-6BB5ACB84416",
                                "country": "IT",
                                "language": "it",
                                "order": 15,
                                "typeDescription": "Sterzo",
                                "subTypeDescription": "-"
                            }
                        }
                    },
                    {
                        "_id": "955F0BC6-96B5-47F1-8C75-6EF91155BC43",
                        "code": "PERFORMANC",
                        "description": "Performance",
                        "typeCode": "PERF_BLANK",
                        "typeDescription": "",
                        "name": "Maximum Speed",
                        "unitOfMeasure": "km/h",
                        "values": [
                            {
                                "_id": "2BD1D929-7192-4337-AE01-0B5974C902F3",
                                "value": "180",
                                "validFrom": "2023-03-01",
                                "validTo": "2999-12-01",
                                "final": None,
                                "languages": {},
                                "translations": {}
                            }
                        ],
                        "languages": {
                            "translations": [
                                "it-IT"
                            ],
                            "types": [
                                "it-IT"
                            ]
                        },
                        "translations": {
                            "it-IT": {
                                "_id": "0854F2A4-CBFE-4E39-A3AC-353C20F2D6D8",
                                "country": "IT",
                                "language": "it",
                                "order": 99,
                                "shortDescription": "Velocità max",
                                "longDescription": "Velocità max",
                                "marketingComment": None,
                                "highlight": False
                            }
                        },
                        "unitOfMeasureTranslations": {},
                        "types": {
                            "it-IT": {
                                "_id": "16633327-4B6D-48C5-A789-BC9FE4556214",
                                "country": "IT",
                                "language": "it",
                                "order": 11,
                                "typeDescription": "Prestazioni",
                                "subTypeDescription": "-"
                            }
                        }
                    },
                    {
                        "_id": "E801E3CB-1C2F-4A9F-9544-4F4955A344B5",
                        "code": "EXT_DIM",
                        "description": "Exterior Dimensions",
                        "typeCode": "EXT_BLANK",
                        "typeDescription": "",
                        "name": "Overhang (rear)",
                        "unitOfMeasure": "mm",
                        "values": [
                            {
                                "_id": "56B7BFEE-2C61-4897-99DC-1141D35DA55D",
                                "value": "865",
                                "validFrom": "2023-03-01",
                                "validTo": "2999-12-01",
                                "final": None,
                                "languages": {},
                                "translations": {}
                            }
                        ],
                        "languages": {
                            "translations": [
                                "it-IT"
                            ],
                            "types": [
                                "it-IT"
                            ]
                        },
                        "translations": {
                            "it-IT": {
                                "_id": "5A7589DA-2A09-426A-A2EF-B508445AC88B",
                                "country": "IT",
                                "language": "it",
                                "order": 172,
                                "shortDescription": "Sbalzo posteriore",
                                "longDescription": "Sbalzo posteriore",
                                "marketingComment": None,
                                "highlight": False
                            }
                        },
                        "unitOfMeasureTranslations": {},
                        "types": {
                            "it-IT": {
                                "_id": "4F2D6E50-BC41-4A23-8426-833ECE779974",
                                "country": "IT",
                                "language": "it",
                                "order": 4,
                                "typeDescription": "Dimensioni esterne",
                                "subTypeDescription": "-"
                            }
                        }
                    },
                    {
                        "_id": "D63360BB-F413-465E-B967-65C1F76E320D",
                        "code": "INT_DIM",
                        "description": "Interior Dimensions",
                        "typeCode": "INT_BLANK",
                        "typeDescription": "",
                        "name": "Headroom (rear)",
                        "unitOfMeasure": "mm",
                        "values": [
                            {
                                "_id": "54A3C826-6C56-4A52-A81A-1957A153BAA4",
                                "value": "32",
                                "validFrom": "2023-03-01",
                                "validTo": "2999-12-01",
                                "final": None,
                                "languages": {},
                                "translations": {}
                            }
                        ],
                        "languages": {
                            "types": [
                                "it-IT"
                            ]
                        },
                        "translations": {},
                        "unitOfMeasureTranslations": {},
                        "types": {
                            "it-IT": {
                                "_id": "73B07E47-489B-435E-B6A1-D1D814FB2434",
                                "country": "IT",
                                "language": "it",
                                "order": 5,
                                "typeDescription": "Dimensioni interne",
                                "subTypeDescription": "-"
                            }
                        }
                    },
                    {
                        "_id": "FA28748C-D215-4D95-96B2-CA04C600D9AD",
                        "code": "OTHER_EMIS",
                        "description": "Other Emissions",
                        "typeCode": "OTH_BLANK",
                        "typeDescription": "",
                        "name": "Carbon Monoxide (CO)",
                        "unitOfMeasure": "mg/km",
                        "values": [
                            {
                                "_id": "D44D0689-1DEF-446B-A23E-19E2FEFCDBB9",
                                "value": "188.8",
                                "validFrom": "2023-03-01",
                                "validTo": "2999-12-01",
                                "final": None,
                                "languages": {},
                                "translations": {}
                            }
                        ],
                        "languages": {
                            "types": [
                                "it-IT"
                            ]
                        },
                        "translations": {},
                        "unitOfMeasureTranslations": {},
                        "types": {
                            "it-IT": {
                                "_id": "5AF52DD9-0DB5-477E-AB75-0EDDDC680D2C",
                                "country": "IT",
                                "language": "it",
                                "order": 1,
                                "typeDescription": "Altre emissioni",
                                "subTypeDescription": "-"
                            }
                        }
                    },
                    {
                        "_id": "661ABBD3-016F-4A74-8A61-A6C7A3E16A9D",
                        "code": "EXT_DIM",
                        "description": "Exterior Dimensions",
                        "typeCode": "EXT_BLANK",
                        "typeDescription": "",
                        "name": "Overall height",
                        "unitOfMeasure": "mm",
                        "values": [
                            {
                                "_id": "B362327E-01E2-422D-B286-1D07B78BAE79",
                                "value": "1620",
                                "validFrom": "2023-03-01",
                                "validTo": "2999-12-01",
                                "final": None,
                                "languages": {},
                                "translations": {}
                            }
                        ],
                        "languages": {
                            "translations": [
                                "it-IT"
                            ],
                            "types": [
                                "it-IT"
                            ]
                        },
                        "translations": {
                            "it-IT": {
                                "_id": "DACCFA96-1B20-4624-A256-000662A5D781",
                                "country": "IT",
                                "language": "it",
                                "order": 167,
                                "shortDescription": "Altezza totale",
                                "longDescription": "Altezza totale",
                                "marketingComment": None,
                                "highlight": False
                            }
                        },
                        "unitOfMeasureTranslations": {},
                        "types": {
                            "it-IT": {
                                "_id": "4F2D6E50-BC41-4A23-8426-833ECE779974",
                                "country": "IT",
                                "language": "it",
                                "order": 4,
                                "typeDescription": "Dimensioni esterne",
                                "subTypeDescription": "-"
                            }
                        }
                    },
                    {
                        "_id": "BFA7A8F9-0B9A-46B4-8390-AD8FBD54A5AD",
                        "code": "OTHER_EMIS",
                        "description": "Other Emissions",
                        "typeCode": "OTH_BLANK",
                        "typeDescription": "",
                        "name": "Exhaust Emissions EC Reg (Update)",
                        "unitOfMeasure": "",
                        "values": [
                            {
                                "_id": "8F78B826-7DA6-48BB-922B-1F2643A6E86E",
                                "value": "2018/1832AP",
                                "validFrom": "2023-03-01",
                                "validTo": "2999-12-01",
                                "final": None,
                                "languages": {},
                                "translations": {}
                            }
                        ],
                        "languages": {
                            "types": [
                                "it-IT"
                            ]
                        },
                        "translations": {},
                        "unitOfMeasureTranslations": {},
                        "types": {
                            "it-IT": {
                                "_id": "5AF52DD9-0DB5-477E-AB75-0EDDDC680D2C",
                                "country": "IT",
                                "language": "it",
                                "order": 1,
                                "typeDescription": "Altre emissioni",
                                "subTypeDescription": "-"
                            }
                        }
                    },
                    {
                        "_id": "2E2B7AF8-E08A-4A18-98F5-0A465DF6CD2B",
                        "code": "TRANSMIS",
                        "description": "Transmission",
                        "typeCode": "TR_BLANK",
                        "typeDescription": "",
                        "name": "Transmission operation type",
                        "unitOfMeasure": "",
                        "values": [
                            {
                                "_id": "1D1C4B39-064C-45FE-8A3C-1F7BB5217F52",
                                "value": "CVT",
                                "validFrom": "2023-03-01",
                                "validTo": "2999-12-01",
                                "final": None,
                                "languages": {},
                                "translations": {}
                            }
                        ],
                        "languages": {
                            "translations": [
                                "it-IT"
                            ],
                            "types": [
                                "it-IT"
                            ]
                        },
                        "translations": {
                            "it-IT": {
                                "_id": "4E8E9D0D-870F-47A6-9509-A212391D7F28",
                                "country": "IT",
                                "language": "it",
                                "order": 132,
                                "shortDescription": "Cambio",
                                "longDescription": "Cambio",
                                "marketingComment": None,
                                "highlight": False
                            }
                        },
                        "unitOfMeasureTranslations": {},
                        "types": {
                            "it-IT": {
                                "_id": "25341A56-E0E6-461E-A387-6A879969708D",
                                "country": "IT",
                                "language": "it",
                                "order": 16,
                                "typeDescription": "Trasmissione",
                                "subTypeDescription": "-"
                            }
                        }
                    },
                    {
                        "_id": "7EEE4382-155B-48DF-8338-07BE2661D213",
                        "code": "ENGINE",
                        "description": "Engine",
                        "typeCode": "ENG_BLANK",
                        "typeDescription": "",
                        "name": "Valve mechanism",
                        "unitOfMeasure": "",
                        "values": [
                            {
                                "_id": "ABCBE280-7BE7-40F2-9B71-203930186C40",
                                "value": "16 valvole DOHC",
                                "validFrom": "2023-03-01",
                                "validTo": "2999-12-01",
                                "final": None,
                                "languages": {},
                                "translations": {}
                            }
                        ],
                        "languages": {
                            "translations": [
                                "it-IT"
                            ],
                            "types": [
                                "it-IT"
                            ]
                        },
                        "translations": {
                            "it-IT": {
                                "_id": "329118B3-A970-49E4-A5FD-55193855A258",
                                "country": "IT",
                                "language": "it",
                                "order": 116,
                                "shortDescription": "Variatore di fase",
                                "longDescription": "Variatore di fase",
                                "marketingComment": None,
                                "highlight": False
                            }
                        },
                        "unitOfMeasureTranslations": {},
                        "types": {
                            "it-IT": {
                                "_id": "94E07105-4196-4D9E-85F1-BC2C93FAC7F1",
                                "country": "IT",
                                "language": "it",
                                "order": 9,
                                "typeDescription": "Motore",
                                "subTypeDescription": "-"
                            }
                        }
                    },
                    {
                        "_id": "7B4B9331-5D6D-4A10-AE09-3D74C3851148",
                        "code": "ENGINE",
                        "description": "Engine",
                        "typeCode": "ENG_BLANK",
                        "typeDescription": "",
                        "name": "Number of cylinders & layout",
                        "unitOfMeasure": "",
                        "values": [
                            {
                                "_id": "948CA2AB-B9A4-485F-9446-2060CD7E4374",
                                "value": "4 in linea",
                                "validFrom": "2023-03-01",
                                "validTo": "2999-12-01",
                                "final": None,
                                "languages": {},
                                "translations": {}
                            }
                        ],
                        "languages": {
                            "translations": [
                                "it-IT"
                            ],
                            "types": [
                                "it-IT"
                            ]
                        },
                        "translations": {
                            "it-IT": {
                                "_id": "7B0BA639-EF42-4751-9884-E4699722ADE8",
                                "country": "IT",
                                "language": "it",
                                "order": 108,
                                "shortDescription": "Numero cilindri",
                                "longDescription": "Numero cilindri",
                                "marketingComment": None,
                                "highlight": False
                            }
                        },
                        "unitOfMeasureTranslations": {},
                        "types": {
                            "it-IT": {
                                "_id": "94E07105-4196-4D9E-85F1-BC2C93FAC7F1",
                                "country": "IT",
                                "language": "it",
                                "order": 9,
                                "typeDescription": "Motore",
                                "subTypeDescription": "-"
                            }
                        }
                    },
                    {
                        "_id": "03349FFB-F9FC-4A75-9844-C485FE2E1E1F",
                        "code": "LUGGAGE",
                        "description": "Luggage Compartment",
                        "typeCode": "LUGG_BLANK",
                        "typeDescription": "",
                        "name": "Luggage room height (up to roof)",
                        "unitOfMeasure": "mm",
                        "values": [
                            {
                                "_id": "E4733403-E665-46C1-A9BF-2123CA171E76",
                                "value": "907",
                                "validFrom": "2023-03-01",
                                "validTo": "2999-12-01",
                                "final": None,
                                "languages": {},
                                "translations": {}
                            }
                        ],
                        "languages": {
                            "types": [
                                "it-IT"
                            ]
                        },
                        "translations": {},
                        "unitOfMeasureTranslations": {},
                        "types": {
                            "it-IT": {
                                "_id": "F344B59E-6151-4C65-9369-26936453B37B",
                                "country": "IT",
                                "language": "it",
                                "order": 2,
                                "typeDescription": "Bagagliaio",
                                "subTypeDescription": "-"
                            }
                        }
                    },
                    {
                        "_id": "1B19C5D5-D222-4D67-874A-845ACA1B73DE",
                        "code": "ENGINE",
                        "description": "Engine",
                        "typeCode": "ENG_BLANK",
                        "typeDescription": "",
                        "name": "Maximum output (hp)",
                        "unitOfMeasure": "DIN hp",
                        "values": [
                            {
                                "_id": "4429874A-70D3-45C4-8525-23801CE7CD3A",
                                "value": "152",
                                "validFrom": "2023-03-01",
                                "validTo": "2999-12-01",
                                "final": None,
                                "languages": {},
                                "translations": {}
                            }
                        ],
                        "languages": {
                            "translations": [
                                "it-IT"
                            ],
                            "types": [
                                "it-IT"
                            ]
                        },
                        "translations": {
                            "it-IT": {
                                "_id": "AF8BB305-8C6F-4DEA-95C5-60619735E492",
                                "country": "IT",
                                "language": "it",
                                "order": 106,
                                "shortDescription": "Potenza max CV",
                                "longDescription": "Potenza max",
                                "marketingComment": None,
                                "highlight": False
                            }
                        },
                        "unitOfMeasureTranslations": {},
                        "types": {
                            "it-IT": {
                                "_id": "94E07105-4196-4D9E-85F1-BC2C93FAC7F1",
                                "country": "IT",
                                "language": "it",
                                "order": 9,
                                "typeDescription": "Motore",
                                "subTypeDescription": "-"
                            }
                        }
                    },
                    {
                        "_id": "E6E10609-A46E-4514-853D-764A259C4D88",
                        "code": "ENGINE",
                        "description": "Engine",
                        "typeCode": "ENG_BLANK",
                        "typeDescription": "",
                        "name": "Min RPM for max torque",
                        "unitOfMeasure": "rpm",
                        "values": [
                            {
                                "_id": "DA2FED28-B33F-4052-938C-2AC076170A7F",
                                "value": "4400",
                                "validFrom": "2023-03-01",
                                "validTo": "2999-12-01",
                                "final": None,
                                "languages": {},
                                "translations": {}
                            }
                        ],
                        "languages": {
                            "types": [
                                "it-IT"
                            ]
                        },
                        "translations": {},
                        "unitOfMeasureTranslations": {},
                        "types": {
                            "it-IT": {
                                "_id": "94E07105-4196-4D9E-85F1-BC2C93FAC7F1",
                                "country": "IT",
                                "language": "it",
                                "order": 9,
                                "typeDescription": "Motore",
                                "subTypeDescription": "-"
                            }
                        }
                    },
                    {
                        "_id": "D0A1049A-8D6A-4B02-84EF-9ED7A715C81A",
                        "code": "LUGGAGE",
                        "description": "Luggage Compartment",
                        "typeCode": "LUGG_BLANK",
                        "typeDescription": "",
                        "name": "VDA capacity up to roof (1st row up)",
                        "unitOfMeasure": "l",
                        "values": [
                            {
                                "_id": "DFDE4E5D-275D-4703-9A62-2F11827711D2",
                                "value": "1337",
                                "validFrom": "2023-03-01",
                                "validTo": "2999-12-01",
                                "final": None,
                                "languages": {},
                                "translations": {}
                            }
                        ],
                        "languages": {
                            "types": [
                                "it-IT"
                            ]
                        },
                        "translations": {},
                        "unitOfMeasureTranslations": {},
                        "types": {
                            "it-IT": {
                                "_id": "F344B59E-6151-4C65-9369-26936453B37B",
                                "country": "IT",
                                "language": "it",
                                "order": 2,
                                "typeDescription": "Bagagliaio",
                                "subTypeDescription": "-"
                            }
                        }
                    },
                    {
                        "_id": "83D93371-54B7-4DDA-936C-F6F9CCBCA25C",
                        "code": "STEERING",
                        "description": "Steering",
                        "typeCode": "STEE_BLANK",
                        "typeDescription": "",
                        "name": "Steering Type",
                        "unitOfMeasure": "",
                        "values": [
                            {
                                "_id": "1747AD9C-EC78-4925-AB80-316F336AA3F6",
                                "value": "Pignone e cremagliera",
                                "validFrom": "2023-03-01",
                                "validTo": "2999-12-01",
                                "final": None,
                                "languages": {},
                                "translations": {}
                            }
                        ],
                        "languages": {
                            "types": [
                                "it-IT"
                            ]
                        },
                        "translations": {},
                        "unitOfMeasureTranslations": {},
                        "types": {
                            "it-IT": {
                                "_id": "A1DF6115-09EA-4431-9B25-6BB5ACB84416",
                                "country": "IT",
                                "language": "it",
                                "order": 15,
                                "typeDescription": "Sterzo",
                                "subTypeDescription": "-"
                            }
                        }
                    },
                    {
                        "_id": "C4E9231E-9D9F-4FF2-B6B2-ECC6DC0A9EC4",
                        "code": "WEIGHT",
                        "description": "Weight",
                        "typeCode": "WEIG_BLANK",
                        "typeDescription": "",
                        "name": "Towing capacity (with brakes)",
                        "unitOfMeasure": "kg",
                        "values": [
                            {
                                "_id": "CBF9EE81-1362-41DC-8505-35FAD9949D4A",
                                "value": "750",
                                "validFrom": "2023-03-01",
                                "validTo": "2999-12-01",
                                "final": None,
                                "languages": {},
                                "translations": {}
                            }
                        ],
                        "languages": {
                            "types": [
                                "it-IT"
                            ]
                        },
                        "translations": {},
                        "unitOfMeasureTranslations": {},
                        "types": {
                            "it-IT": {
                                "_id": "8D8FF346-3DB1-4222-9B51-53CAF38B83D6",
                                "country": "IT",
                                "language": "it",
                                "order": 10,
                                "typeDescription": "Pesi",
                                "subTypeDescription": "-"
                            }
                        }
                    },
                    {
                        "_id": "CF65BD38-CA79-463A-9647-47FD7A55ADA5",
                        "code": "SUSPENSION",
                        "description": "Suspension",
                        "typeCode": "SUS_BLANK",
                        "typeDescription": "",
                        "name": "Front Axle Track",
                        "unitOfMeasure": "mm",
                        "values": [
                            {
                                "_id": "4656FCE0-6B85-4409-8570-3AFBEE9AD940",
                                "value": "1560",
                                "validFrom": "2023-03-01",
                                "validTo": "2999-12-01",
                                "final": None,
                                "languages": {},
                                "translations": {}
                            }
                        ],
                        "languages": {
                            "types": [
                                "it-IT"
                            ]
                        },
                        "translations": {},
                        "unitOfMeasureTranslations": {},
                        "types": {
                            "it-IT": {
                                "_id": "BF7A6902-C9C9-4586-B97F-48621CE05BDC",
                                "country": "IT",
                                "language": "it",
                                "order": 14,
                                "typeDescription": "Sospensioni",
                                "subTypeDescription": "-"
                            }
                        }
                    },
                    {
                        "_id": "26477645-22E1-4ADB-A344-B30C3BEEA39A",
                        "code": "GENERAL",
                        "description": "General",
                        "typeCode": "GEN_BLANK",
                        "typeDescription": "",
                        "name": "The metric/imperial units for the speedometer",
                        "unitOfMeasure": "",
                        "values": [
                            {
                                "_id": "74B7D6C6-0338-4189-9A64-3BBB77005FA5",
                                "value": "Metrico",
                                "validFrom": "2023-03-01",
                                "validTo": "2999-12-01",
                                "final": None,
                                "languages": {},
                                "translations": {}
                            }
                        ],
                        "languages": {},
                        "translations": {},
                        "unitOfMeasureTranslations": {},
                        "types": {}
                    },
                    {
                        "_id": "078601A5-0688-4FEF-8AA0-520BEEC4DC44",
                        "code": "ENGINE",
                        "description": "Engine",
                        "typeCode": "ENG_BLANK",
                        "typeDescription": "",
                        "name": "Displacement",
                        "unitOfMeasure": "cc",
                        "values": [
                            {
                                "_id": "DBF3259D-1054-4020-91FF-3C6C4FB2C973",
                                "value": "1987",
                                "validFrom": "2023-03-01",
                                "validTo": "2999-12-01",
                                "final": None,
                                "languages": {},
                                "translations": {}
                            }
                        ],
                        "languages": {
                            "translations": [
                                "it-IT"
                            ],
                            "types": [
                                "it-IT"
                            ]
                        },
                        "translations": {
                            "it-IT": {
                                "_id": "23470D91-777D-4099-961C-DBCA08A407A8",
                                "country": "IT",
                                "language": "it",
                                "order": 103,
                                "shortDescription": "Cilindrata",
                                "longDescription": "Cilindrata",
                                "marketingComment": None,
                                "highlight": False
                            }
                        },
                        "unitOfMeasureTranslations": {},
                        "types": {
                            "it-IT": {
                                "_id": "94E07105-4196-4D9E-85F1-BC2C93FAC7F1",
                                "country": "IT",
                                "language": "it",
                                "order": 9,
                                "typeDescription": "Motore",
                                "subTypeDescription": "-"
                            }
                        }
                    },
                    {
                        "_id": "29871369-65BD-4BD6-A194-E658A5D27B6D",
                        "code": "LUGGAGE",
                        "description": "Luggage Compartment",
                        "typeCode": "LUGG_BLANK",
                        "typeDescription": "",
                        "name": "VDA capa up to tonneau cover (1st & 2nd rows up)",
                        "unitOfMeasure": "l",
                        "values": [
                            {
                                "_id": "0080DD7F-3854-41FC-AE13-3CA2BACD4D8A",
                                "value": "425",
                                "validFrom": "2023-03-01",
                                "validTo": "2999-12-01",
                                "final": None,
                                "languages": {},
                                "translations": {}
                            }
                        ],
                        "languages": {
                            "types": [
                                "it-IT"
                            ]
                        },
                        "translations": {},
                        "unitOfMeasureTranslations": {},
                        "types": {
                            "it-IT": {
                                "_id": "F344B59E-6151-4C65-9369-26936453B37B",
                                "country": "IT",
                                "language": "it",
                                "order": 2,
                                "typeDescription": "Bagagliaio",
                                "subTypeDescription": "-"
                            }
                        }
                    },
                    {
                        "_id": "8955E6C9-5AED-4FCD-8C41-4DFA5AA8788D",
                        "code": "EXT_DIM",
                        "description": "Exterior Dimensions",
                        "typeCode": "EXT_BLANK",
                        "typeDescription": "",
                        "name": "Ground clearance",
                        "unitOfMeasure": "mm",
                        "values": [
                            {
                                "_id": "87DFECE9-1F9C-453B-B02E-3DCEA7ABD654",
                                "value": "160",
                                "validFrom": "2023-03-01",
                                "validTo": "2999-12-01",
                                "final": None,
                                "languages": {},
                                "translations": {}
                            }
                        ],
                        "languages": {
                            "translations": [
                                "it-IT"
                            ],
                            "types": [
                                "it-IT"
                            ]
                        },
                        "translations": {
                            "it-IT": {
                                "_id": "2E99D061-6987-44BC-8FFF-B81DA9D16F72",
                                "country": "IT",
                                "language": "it",
                                "order": 162,
                                "shortDescription": "Altezza da terra",
                                "longDescription": "Altezza da terra",
                                "marketingComment": None,
                                "highlight": False
                            }
                        },
                        "unitOfMeasureTranslations": {},
                        "types": {
                            "it-IT": {
                                "_id": "4F2D6E50-BC41-4A23-8426-833ECE779974",
                                "country": "IT",
                                "language": "it",
                                "order": 4,
                                "typeDescription": "Dimensioni esterne",
                                "subTypeDescription": "-"
                            }
                        }
                    },
                    {
                        "_id": "94FD8BEE-FE2D-4874-8FAA-7BB7DF40F065",
                        "code": "WEIGHT",
                        "description": "Weight",
                        "typeCode": "WEIG_MASS",
                        "typeDescription": "Gross vehicle mass",
                        "name": "Gross vehicle weight",
                        "unitOfMeasure": "kg",
                        "values": [
                            {
                                "_id": "C3163C0D-CE8F-457D-96E0-3DEF2B6728EF",
                                "value": "1970",
                                "validFrom": "2023-03-01",
                                "validTo": "2999-12-01",
                                "final": None,
                                "languages": {},
                                "translations": {}
                            }
                        ],
                        "languages": {
                            "types": [
                                "it-IT"
                            ]
                        },
                        "translations": {},
                        "unitOfMeasureTranslations": {},
                        "types": {
                            "it-IT": {
                                "_id": "8D8FF346-3DB1-4222-9B51-53CAF38B83D6",
                                "country": "IT",
                                "language": "it",
                                "order": 10,
                                "typeDescription": "Pesi",
                                "subTypeDescription": "-"
                            }
                        }
                    },
                    {
                        "_id": "E89D0255-CDF0-4C1D-A73E-8D750877AB66",
                        "code": "GENERAL",
                        "description": "General",
                        "typeCode": "GEN_BLANK",
                        "typeDescription": "",
                        "name": "The type approval number",
                        "unitOfMeasure": "",
                        "values": [
                            {
                                "_id": "84D293AE-41C4-49B3-8293-3EAEB6812943",
                                "value": "e6*2018/858*00186*00",
                                "validFrom": "2023-03-01",
                                "validTo": "2999-12-01",
                                "final": None,
                                "languages": {},
                                "translations": {}
                            }
                        ],
                        "languages": {},
                        "translations": {},
                        "unitOfMeasureTranslations": {},
                        "types": {}
                    },
                    {
                        "_id": "507B972C-7AD8-4306-B40A-79410E31076C",
                        "code": "ENGINE",
                        "description": "Engine",
                        "typeCode": "ENG_BLANK",
                        "typeDescription": "",
                        "name": "Maximum torque",
                        "unitOfMeasure": "Nm",
                        "values": [
                            {
                                "_id": "17888509-6E6D-416D-81F4-3F175B3A9BF1",
                                "value": "190",
                                "validFrom": "2023-03-01",
                                "validTo": "2999-12-01",
                                "final": None,
                                "languages": {},
                                "translations": {}
                            }
                        ],
                        "languages": {
                            "types": [
                                "it-IT"
                            ]
                        },
                        "translations": {},
                        "unitOfMeasureTranslations": {},
                        "types": {
                            "it-IT": {
                                "_id": "94E07105-4196-4D9E-85F1-BC2C93FAC7F1",
                                "country": "IT",
                                "language": "it",
                                "order": 9,
                                "typeDescription": "Motore",
                                "subTypeDescription": "-"
                            }
                        }
                    },
                    {
                        "_id": "FC560170-8978-4CBB-9022-C47FB933441B",
                        "code": "STEERING",
                        "description": "Steering",
                        "typeCode": "STEE_BLANK",
                        "typeDescription": "",
                        "name": "Power steering system",
                        "unitOfMeasure": "",
                        "values": [
                            {
                                "_id": "A22EEAD0-8E21-40F9-80C4-403AF68C51A4",
                                "value": "Electrico",
                                "validFrom": "2023-03-01",
                                "validTo": "2999-12-01",
                                "final": None,
                                "languages": {},
                                "translations": {}
                            }
                        ],
                        "languages": {
                            "translations": [
                                "it-IT"
                            ],
                            "types": [
                                "it-IT"
                            ]
                        },
                        "translations": {
                            "it-IT": {
                                "_id": "DE1092F8-3431-4715-842F-33E7DE61C952",
                                "country": "IT",
                                "language": "it",
                                "order": 148,
                                "shortDescription": "Servosterzo",
                                "longDescription": "Servosterzo",
                                "marketingComment": None,
                                "highlight": False
                            }
                        },
                        "unitOfMeasureTranslations": {},
                        "types": {
                            "it-IT": {
                                "_id": "A1DF6115-09EA-4431-9B25-6BB5ACB84416",
                                "country": "IT",
                                "language": "it",
                                "order": 15,
                                "typeDescription": "Sterzo",
                                "subTypeDescription": "-"
                            }
                        }
                    },
                    {
                        "_id": "D35B2620-0743-41ED-BB6E-07B2186B4EEE",
                        "code": "LUGGAGE",
                        "description": "Luggage Compartment",
                        "typeCode": "LUGG_BLANK",
                        "typeDescription": "",
                        "name": "Luggage room max.width",
                        "unitOfMeasure": "mm",
                        "values": [
                            {
                                "_id": "CBDCC1C7-7508-4C5A-AC7A-406A3CDD5D66",
                                "value": "1375",
                                "validFrom": "2023-03-01",
                                "validTo": "2999-12-01",
                                "final": None,
                                "languages": {},
                                "translations": {}
                            }
                        ],
                        "languages": {
                            "types": [
                                "it-IT"
                            ]
                        },
                        "translations": {},
                        "unitOfMeasureTranslations": {},
                        "types": {
                            "it-IT": {
                                "_id": "F344B59E-6151-4C65-9369-26936453B37B",
                                "country": "IT",
                                "language": "it",
                                "order": 2,
                                "typeDescription": "Bagagliaio",
                                "subTypeDescription": "-"
                            }
                        }
                    },
                    {
                        "_id": "93B7E165-CCD3-4FE5-A030-7CD028866BA0",
                        "code": "LUGGAGE",
                        "description": "Luggage Compartment",
                        "typeCode": "LUGG_BLANK",
                        "typeDescription": "",
                        "name": "VDA capacity up to roof (1st & 2nd rows up)",
                        "unitOfMeasure": "l",
                        "values": [
                            {
                                "_id": "EDA5760B-6501-474D-9E90-415B6271DACA",
                                "value": "549",
                                "validFrom": "2023-03-01",
                                "validTo": "2999-12-01",
                                "final": None,
                                "languages": {},
                                "translations": {}
                            }
                        ],
                        "languages": {
                            "types": [
                                "it-IT"
                            ]
                        },
                        "translations": {},
                        "unitOfMeasureTranslations": {},
                        "types": {
                            "it-IT": {
                                "_id": "F344B59E-6151-4C65-9369-26936453B37B",
                                "country": "IT",
                                "language": "it",
                                "order": 2,
                                "typeDescription": "Bagagliaio",
                                "subTypeDescription": "-"
                            }
                        }
                    },
                    {
                        "_id": "3F6BA1CF-CBA0-4196-BB6B-6C670E682DFD",
                        "code": "FUEL_CONS",
                        "description": "Fuel Consumption",
                        "typeCode": "FUEL_BLANK",
                        "typeDescription": "",
                        "name": "Combined",
                        "unitOfMeasure": "l/100km",
                        "values": [
                            {
                                "_id": "221D3C42-0D82-49EB-B50A-46FC8F76B84D",
                                "value": "4.96",
                                "validFrom": "2023-03-01",
                                "validTo": "2999-12-01",
                                "final": None,
                                "languages": {},
                                "translations": {}
                            }
                        ],
                        "languages": {
                            "translations": [
                                "it-IT"
                            ],
                            "types": [
                                "it-IT"
                            ]
                        },
                        "translations": {
                            "it-IT": {
                                "_id": "C4E3C21E-D788-4D61-B985-8859A95C10AA",
                                "country": "IT",
                                "language": "it",
                                "order": 133,
                                "shortDescription": "Combinato",
                                "longDescription": "Combinato",
                                "marketingComment": None,
                                "highlight": False
                            }
                        },
                        "unitOfMeasureTranslations": {},
                        "types": {
                            "it-IT": {
                                "_id": "A5023D92-7A67-4B22-AEF3-7D5CDCB0AE1A",
                                "country": "IT",
                                "language": "it",
                                "order": 3,
                                "typeDescription": "Consumi",
                                "subTypeDescription": "-"
                            }
                        }
                    },
                    {
                        "_id": "ABEFAF59-E17C-4640-8524-5A8948DA04FB",
                        "code": "WEIGHT",
                        "description": "Weight",
                        "typeCode": "WEIG_KERB",
                        "typeDescription": "Kerb weight",
                        "name": "Kerb weight minimum",
                        "unitOfMeasure": "kg",
                        "values": [
                            {
                                "_id": "F8681B53-3D75-4184-943E-48793519AB1C",
                                "value": "1445",
                                "validFrom": "2023-03-01",
                                "validTo": "2999-12-01",
                                "final": None,
                                "languages": {},
                                "translations": {}
                            }
                        ],
                        "languages": {
                            "translations": [
                                "it-IT"
                            ],
                            "types": [
                                "it-IT"
                            ]
                        },
                        "translations": {
                            "it-IT": {
                                "_id": "C6B9AD25-A799-4502-B386-C4C15D3E932F",
                                "country": "IT",
                                "language": "it",
                                "order": 197,
                                "shortDescription": "Massa in ordine di marcia",
                                "longDescription": "Massa in ordine di marcia",
                                "marketingComment": None,
                                "highlight": False
                            }
                        },
                        "unitOfMeasureTranslations": {},
                        "types": {
                            "it-IT": {
                                "_id": "8D8FF346-3DB1-4222-9B51-53CAF38B83D6",
                                "country": "IT",
                                "language": "it",
                                "order": 10,
                                "typeDescription": "Pesi",
                                "subTypeDescription": "-"
                            }
                        }
                    },
                    {
                        "_id": "263788E7-329A-4AFD-86F9-B0874BD2857C",
                        "code": "ENGINE",
                        "description": "Engine",
                        "typeCode": "ENG_BLANK",
                        "typeDescription": "",
                        "name": "Stroke",
                        "unitOfMeasure": "mm",
                        "values": [
                            {
                                "_id": "30AC0F2B-0E4D-4C1C-B63C-48D27C173A3C",
                                "value": "97.6",
                                "validFrom": "2023-03-01",
                                "validTo": "2999-12-01",
                                "final": None,
                                "languages": {},
                                "translations": {}
                            }
                        ],
                        "languages": {
                            "types": [
                                "it-IT"
                            ]
                        },
                        "translations": {},
                        "unitOfMeasureTranslations": {},
                        "types": {
                            "it-IT": {
                                "_id": "94E07105-4196-4D9E-85F1-BC2C93FAC7F1",
                                "country": "IT",
                                "language": "it",
                                "order": 9,
                                "typeDescription": "Motore",
                                "subTypeDescription": "-"
                            }
                        }
                    },
                    {
                        "_id": "1063995D-83ED-41AB-B0D5-4E238027F0A0",
                        "code": "SUSPENSION",
                        "description": "Suspension",
                        "typeCode": "SUS_BLANK",
                        "typeDescription": "",
                        "name": "Front Suspension",
                        "unitOfMeasure": "",
                        "values": [
                            {
                                "_id": "3782BC90-305C-4417-AC0E-48D6DAFC0BEA",
                                "value": "Macpherson",
                                "validFrom": "2023-03-01",
                                "validTo": "2999-12-01",
                                "final": None,
                                "languages": {},
                                "translations": {}
                            }
                        ],
                        "languages": {
                            "translations": [
                                "it-IT"
                            ],
                            "types": [
                                "it-IT"
                            ]
                        },
                        "translations": {
                            "it-IT": {
                                "_id": "FCD492A9-C821-46E8-88C0-F91D4AEEA87E",
                                "country": "IT",
                                "language": "it",
                                "order": 142,
                                "shortDescription": "Sospensioni anteriori",
                                "longDescription": "Sospensioni anteriori",
                                "marketingComment": None,
                                "highlight": False
                            }
                        },
                        "unitOfMeasureTranslations": {},
                        "types": {
                            "it-IT": {
                                "_id": "BF7A6902-C9C9-4586-B97F-48621CE05BDC",
                                "country": "IT",
                                "language": "it",
                                "order": 14,
                                "typeDescription": "Sospensioni",
                                "subTypeDescription": "-"
                            }
                        }
                    },
                    {
                        "_id": "D2115C82-FA7E-43B7-97D4-B3F07EE58DE5",
                        "code": "WEIGHT",
                        "description": "Weight",
                        "typeCode": "WEIG_BLANK",
                        "typeDescription": "",
                        "name": "Towing capacity (w/o brakes)",
                        "unitOfMeasure": "kg",
                        "values": [
                            {
                                "_id": "BF6EC778-7436-475B-BBC2-49838C87A302",
                                "value": "750",
                                "validFrom": "2023-03-01",
                                "validTo": "2999-12-01",
                                "final": None,
                                "languages": {},
                                "translations": {}
                            }
                        ],
                        "languages": {
                            "types": [
                                "it-IT"
                            ]
                        },
                        "translations": {},
                        "unitOfMeasureTranslations": {},
                        "types": {
                            "it-IT": {
                                "_id": "8D8FF346-3DB1-4222-9B51-53CAF38B83D6",
                                "country": "IT",
                                "language": "it",
                                "order": 10,
                                "typeDescription": "Pesi",
                                "subTypeDescription": "-"
                            }
                        }
                    },
                    {
                        "_id": "1420F7A5-2C10-4BC9-935D-9144569890E1",
                        "code": "WEIGHT",
                        "description": "Weight",
                        "typeCode": "WEIG_BLANK",
                        "typeDescription": "",
                        "name": "Vertical load",
                        "unitOfMeasure": "kg",
                        "values": [
                            {
                                "_id": "9971E51C-6F50-4167-9C94-4FEEF8390A13",
                                "value": "75",
                                "validFrom": "2023-03-01",
                                "validTo": "2999-12-01",
                                "final": None,
                                "languages": {},
                                "translations": {}
                            }
                        ],
                        "languages": {
                            "types": [
                                "it-IT"
                            ]
                        },
                        "translations": {},
                        "unitOfMeasureTranslations": {},
                        "types": {
                            "it-IT": {
                                "_id": "8D8FF346-3DB1-4222-9B51-53CAF38B83D6",
                                "country": "IT",
                                "language": "it",
                                "order": 10,
                                "typeDescription": "Pesi",
                                "subTypeDescription": "-"
                            }
                        }
                    },
                    {
                        "_id": "8B57D6C4-969E-4A79-8A50-29EFC3BA30D7",
                        "code": "LUGGAGE",
                        "description": "Luggage Compartment",
                        "typeCode": "LUGG_BLANK",
                        "typeDescription": "",
                        "name": "Luggage room length (1st row up)",
                        "unitOfMeasure": "",
                        "values": [
                            {
                                "_id": "B0FA1648-DF40-4603-A9F3-503563EA95EA",
                                "value": "1621",
                                "validFrom": "2023-03-01",
                                "validTo": "2999-12-01",
                                "final": None,
                                "languages": {},
                                "translations": {}
                            }
                        ],
                        "languages": {
                            "types": [
                                "it-IT"
                            ]
                        },
                        "translations": {},
                        "unitOfMeasureTranslations": {},
                        "types": {
                            "it-IT": {
                                "_id": "F344B59E-6151-4C65-9369-26936453B37B",
                                "country": "IT",
                                "language": "it",
                                "order": 2,
                                "typeDescription": "Bagagliaio",
                                "subTypeDescription": "-"
                            }
                        }
                    },
                    {
                        "_id": "B74FBA8D-74F4-4090-8F7B-86E570889C0F",
                        "code": "WEIGHT",
                        "description": "Weight",
                        "typeCode": "WEIG_BLANK",
                        "typeDescription": "",
                        "name": "Axle capacity rear",
                        "unitOfMeasure": "kg",
                        "values": [
                            {
                                "_id": "B28308C3-9DCD-4697-B0C3-53260E31FE58",
                                "value": "1100",
                                "validFrom": "2023-03-01",
                                "validTo": "2999-12-01",
                                "final": None,
                                "languages": {},
                                "translations": {}
                            }
                        ],
                        "languages": {
                            "types": [
                                "it-IT"
                            ]
                        },
                        "translations": {},
                        "unitOfMeasureTranslations": {},
                        "types": {
                            "it-IT": {
                                "_id": "8D8FF346-3DB1-4222-9B51-53CAF38B83D6",
                                "country": "IT",
                                "language": "it",
                                "order": 10,
                                "typeDescription": "Pesi",
                                "subTypeDescription": "-"
                            }
                        }
                    },
                    {
                        "_id": "22A29CC2-D7C7-46B1-8BB9-062E0071FB4F",
                        "code": "BRAKES",
                        "description": "Brakes",
                        "typeCode": "BRAK_BLANK",
                        "typeDescription": "",
                        "name": "Brake type front",
                        "unitOfMeasure": "",
                        "values": [
                            {
                                "_id": "32DE1D43-60F5-4448-B085-542BE1085A5B",
                                "value": "Disco Ventilato",
                                "validFrom": "2023-03-01",
                                "validTo": "2999-12-01",
                                "final": None,
                                "languages": {},
                                "translations": {}
                            }
                        ],
                        "languages": {
                            "translations": [
                                "it-IT"
                            ],
                            "types": [
                                "it-IT"
                            ]
                        },
                        "translations": {
                            "it-IT": {
                                "_id": "9A9DF7B0-ABFA-411E-B228-FB70595FBC08",
                                "country": "IT",
                                "language": "it",
                                "order": 144,
                                "shortDescription": "Freni anteriori",
                                "longDescription": "Freni anteriori",
                                "marketingComment": None,
                                "highlight": False
                            }
                        },
                        "unitOfMeasureTranslations": {},
                        "types": {
                            "it-IT": {
                                "_id": "163D3D94-8B08-488C-AE79-1BF872DE08CE",
                                "country": "IT",
                                "language": "it",
                                "order": 8,
                                "typeDescription": "Freni",
                                "subTypeDescription": "-"
                            }
                        }
                    },
                    {
                        "_id": "B8290958-755E-4CEB-A023-76239569864D",
                        "code": "OTHER_EMIS",
                        "description": "Other Emissions",
                        "typeCode": "OTH_BLANK",
                        "typeDescription": "",
                        "name": "Particulates (PM)",
                        "unitOfMeasure": "mg/km",
                        "values": [
                            {
                                "_id": "6F78B93E-8C60-497A-9F1C-5DA23A076F42",
                                "value": "0.13",
                                "validFrom": "2023-03-01",
                                "validTo": "2999-12-01",
                                "final": None,
                                "languages": {},
                                "translations": {}
                            }
                        ],
                        "languages": {
                            "types": [
                                "it-IT"
                            ]
                        },
                        "translations": {},
                        "unitOfMeasureTranslations": {},
                        "types": {
                            "it-IT": {
                                "_id": "5AF52DD9-0DB5-477E-AB75-0EDDDC680D2C",
                                "country": "IT",
                                "language": "it",
                                "order": 1,
                                "typeDescription": "Altre emissioni",
                                "subTypeDescription": "-"
                            }
                        }
                    },
                    {
                        "_id": "5A96BF6F-1F78-478A-9D11-75A95FB431E6",
                        "code": "WEIGHT",
                        "description": "Weight",
                        "typeCode": "WEIG_KERB",
                        "typeDescription": "Kerb weight",
                        "name": "Kerb weight maximum",
                        "unitOfMeasure": "kg",
                        "values": [
                            {
                                "_id": "4AB85C79-601A-484A-8F73-5E8C46AAF937",
                                "value": "1505",
                                "validFrom": "2023-03-01",
                                "validTo": "2999-12-01",
                                "final": None,
                                "languages": {},
                                "translations": {}
                            }
                        ],
                        "languages": {
                            "types": [
                                "it-IT"
                            ]
                        },
                        "translations": {},
                        "unitOfMeasureTranslations": {},
                        "types": {
                            "it-IT": {
                                "_id": "8D8FF346-3DB1-4222-9B51-53CAF38B83D6",
                                "country": "IT",
                                "language": "it",
                                "order": 10,
                                "typeDescription": "Pesi",
                                "subTypeDescription": "-"
                            }
                        }
                    },
                    {
                        "_id": "D1C9EBA7-3CB8-44FE-9F44-FB38740656A2",
                        "code": "OTHER_EMIS",
                        "description": "Other Emissions",
                        "typeCode": "OTH_BLANK",
                        "typeDescription": "",
                        "name": "Euro Class",
                        "unitOfMeasure": "",
                        "values": [
                            {
                                "_id": "67D32201-4C0D-4F35-AB96-65FB24167A1F",
                                "value": "Euro 6 AP",
                                "validFrom": "2023-03-01",
                                "validTo": "2999-12-01",
                                "final": None,
                                "languages": {},
                                "translations": {}
                            }
                        ],
                        "languages": {
                            "translations": [
                                "it-IT"
                            ],
                            "types": [
                                "it-IT"
                            ]
                        },
                        "translations": {
                            "it-IT": {
                                "_id": "2F807EA1-3E9E-4274-A17D-423D94294F92",
                                "country": "IT",
                                "language": "it",
                                "order": 118,
                                "shortDescription": "Classe di emissioni",
                                "longDescription": "Classe di emissioni",
                                "marketingComment": None,
                                "highlight": False
                            }
                        },
                        "unitOfMeasureTranslations": {},
                        "types": {
                            "it-IT": {
                                "_id": "5AF52DD9-0DB5-477E-AB75-0EDDDC680D2C",
                                "country": "IT",
                                "language": "it",
                                "order": 1,
                                "typeDescription": "Altre emissioni",
                                "subTypeDescription": "-"
                            }
                        }
                    },
                    {
                        "_id": "E4B6B8F9-E195-4116-B621-390F00E15D43",
                        "code": "WEIGHT",
                        "description": "Weight",
                        "typeCode": "WEIG_BLANK",
                        "typeDescription": "",
                        "name": "Axle capacity front",
                        "unitOfMeasure": "kg",
                        "values": [
                            {
                                "_id": "8CEA1964-6BD4-4ABE-AA20-66A9A0B4FA76",
                                "value": "1150",
                                "validFrom": "2023-03-01",
                                "validTo": "2999-12-01",
                                "final": None,
                                "languages": {},
                                "translations": {}
                            }
                        ],
                        "languages": {
                            "types": [
                                "it-IT"
                            ]
                        },
                        "translations": {},
                        "unitOfMeasureTranslations": {},
                        "types": {
                            "it-IT": {
                                "_id": "8D8FF346-3DB1-4222-9B51-53CAF38B83D6",
                                "country": "IT",
                                "language": "it",
                                "order": 10,
                                "typeDescription": "Pesi",
                                "subTypeDescription": "-"
                            }
                        }
                    },
                    {
                        "_id": "7F07ADAB-BC29-4342-988C-0F026F67BC12",
                        "code": "HYBRID_SYS",
                        "description": "Hybrid System",
                        "typeCode": "HYB_SYSBAT",
                        "typeDescription": "Hybrid system battery",
                        "name": "Hybrid system battery Type",
                        "unitOfMeasure": "",
                        "values": [
                            {
                                "_id": "86E90BF9-3FBE-41D7-BC76-68B58BE212DB",
                                "value": "lithium-ion",
                                "validFrom": "2023-03-01",
                                "validTo": "2999-12-01",
                                "final": None,
                                "languages": {},
                                "translations": {}
                            }
                        ],
                        "languages": {
                            "translations": [
                                "it-IT"
                            ],
                            "types": [
                                "it-IT"
                            ]
                        },
                        "translations": {
                            "it-IT": {
                                "_id": "A3F27FDC-DBCF-4C3E-9597-6066F52F3672",
                                "country": "IT",
                                "language": "it",
                                "order": 111,
                                "shortDescription": "Batterie HV: tipo",
                                "longDescription": "Batterie HV: tipo",
                                "marketingComment": None,
                                "highlight": False
                            }
                        },
                        "unitOfMeasureTranslations": {},
                        "types": {
                            "it-IT": {
                                "_id": "54C1C52D-8F35-49AB-B5F5-CDE47DCEF46D",
                                "country": "IT",
                                "language": "it",
                                "order": 13,
                                "typeDescription": "Sistema Ibrido / Sistema Fuel Cell",
                                "subTypeDescription": "-"
                            }
                        }
                    },
                    {
                        "_id": "C0236A25-1B3F-4BD4-A9AF-0505A6DEC7DA",
                        "code": "LUGGAGE",
                        "description": "Luggage Compartment",
                        "typeCode": "LUGG_BLANK",
                        "typeDescription": "",
                        "name": "Boot capacity (communicated value)",
                        "unitOfMeasure": "l",
                        "values": [
                            {
                                "_id": "5BD864CA-81AB-4C62-AA44-6EB64076C9B2",
                                "value": "425",
                                "validFrom": "2023-03-01",
                                "validTo": "2999-12-01",
                                "final": None,
                                "languages": {},
                                "translations": {}
                            }
                        ],
                        "languages": {
                            "types": [
                                "it-IT"
                            ]
                        },
                        "translations": {},
                        "unitOfMeasureTranslations": {},
                        "types": {
                            "it-IT": {
                                "_id": "F344B59E-6151-4C65-9369-26936453B37B",
                                "country": "IT",
                                "language": "it",
                                "order": 2,
                                "typeDescription": "Bagagliaio",
                                "subTypeDescription": "-"
                            }
                        }
                    },
                    {
                        "_id": "088030D7-6C59-4A4C-BD57-D265C97444DB",
                        "code": "FUEL_CONS",
                        "description": "Fuel Consumption",
                        "typeCode": "FUEL_BLANK",
                        "typeDescription": "",
                        "name": "Fuel tank capacity",
                        "unitOfMeasure": "l",
                        "values": [
                            {
                                "_id": "BAE30E0C-7F40-4FF1-A03A-6EF8D3115194",
                                "value": "43",
                                "validFrom": "2023-03-01",
                                "validTo": "2999-12-01",
                                "final": None,
                                "languages": {},
                                "translations": {}
                            }
                        ],
                        "languages": {
                            "translations": [
                                "it-IT"
                            ],
                            "types": [
                                "it-IT"
                            ]
                        },
                        "translations": {
                            "it-IT": {
                                "_id": "7A323900-189F-4B87-9CE9-DE69F7024553",
                                "country": "IT",
                                "language": "it",
                                "order": 137,
                                "shortDescription": "Capacità serbatoio carburante",
                                "longDescription": "Capacità serbatoio carburante",
                                "marketingComment": None,
                                "highlight": False
                            }
                        },
                        "unitOfMeasureTranslations": {},
                        "types": {
                            "it-IT": {
                                "_id": "A5023D92-7A67-4B22-AEF3-7D5CDCB0AE1A",
                                "country": "IT",
                                "language": "it",
                                "order": 3,
                                "typeDescription": "Consumi",
                                "subTypeDescription": "-"
                            }
                        }
                    },
                    {
                        "_id": "6B02E327-6A60-41A1-9B8B-E37B73DC07DB",
                        "code": "EXT_DIM",
                        "description": "Exterior Dimensions",
                        "typeCode": "EXT_BLANK",
                        "typeDescription": "",
                        "name": "Overall length",
                        "unitOfMeasure": "mm",
                        "values": [
                            {
                                "_id": "FA3548EE-0C27-435E-83AF-6FCE292B28F6",
                                "value": "4460",
                                "validFrom": "2023-03-01",
                                "validTo": "2999-12-01",
                                "final": None,
                                "languages": {},
                                "translations": {}
                            }
                        ],
                        "languages": {
                            "translations": [
                                "it-IT"
                            ],
                            "types": [
                                "it-IT"
                            ]
                        },
                        "translations": {
                            "it-IT": {
                                "_id": "37B5D159-3AD8-4BE7-8000-3044FAB06469",
                                "country": "IT",
                                "language": "it",
                                "order": 168,
                                "shortDescription": "Lunghezza totale",
                                "longDescription": "Lunghezza totale",
                                "marketingComment": None,
                                "highlight": False
                            }
                        },
                        "unitOfMeasureTranslations": {},
                        "types": {
                            "it-IT": {
                                "_id": "4F2D6E50-BC41-4A23-8426-833ECE779974",
                                "country": "IT",
                                "language": "it",
                                "order": 4,
                                "typeDescription": "Dimensioni esterne",
                                "subTypeDescription": "-"
                            }
                        }
                    },
                    {
                        "_id": "6FB9C5FB-DB79-4407-BC4B-EA34FF99B8CA",
                        "code": "STEERING",
                        "description": "Steering",
                        "typeCode": "STEE_BLANK",
                        "typeDescription": "",
                        "name": "Minimum turning radius (wall)",
                        "unitOfMeasure": "m",
                        "values": [
                            {
                                "_id": "CE504FE8-6247-4950-9B7E-70BC269CB5F5",
                                "value": "5.6",
                                "validFrom": "2023-03-01",
                                "validTo": "2999-12-01",
                                "final": None,
                                "languages": {},
                                "translations": {}
                            }
                        ],
                        "languages": {
                            "translations": [
                                "it-IT"
                            ],
                            "types": [
                                "it-IT"
                            ]
                        },
                        "translations": {
                            "it-IT": {
                                "_id": "DD96F452-D5FD-45DF-B617-50A26DFBC7D8",
                                "country": "IT",
                                "language": "it",
                                "order": 147,
                                "shortDescription": "Raggio di sterzata marciapiede",
                                "longDescription": "Raggio di sterzata",
                                "marketingComment": None,
                                "highlight": False
                            }
                        },
                        "unitOfMeasureTranslations": {},
                        "types": {
                            "it-IT": {
                                "_id": "A1DF6115-09EA-4431-9B25-6BB5ACB84416",
                                "country": "IT",
                                "language": "it",
                                "order": 15,
                                "typeDescription": "Sterzo",
                                "subTypeDescription": "-"
                            }
                        }
                    },
                    {
                        "_id": "02BC49DE-4960-4694-852F-8AAB5DC1DEE6",
                        "code": "OTHER_EMIS",
                        "description": "Other Emissions",
                        "typeCode": "OTH_BLANK",
                        "typeDescription": "",
                        "name": "NMHC non-methan Hydrocarbons",
                        "unitOfMeasure": "mg/km",
                        "values": [
                            {
                                "_id": "94FE160F-E5D7-43A7-BDBE-72EDA96B083E",
                                "value": "15.7",
                                "validFrom": "2023-03-01",
                                "validTo": "2999-12-01",
                                "final": None,
                                "languages": {},
                                "translations": {}
                            }
                        ],
                        "languages": {
                            "types": [
                                "it-IT"
                            ]
                        },
                        "translations": {},
                        "unitOfMeasureTranslations": {},
                        "types": {
                            "it-IT": {
                                "_id": "5AF52DD9-0DB5-477E-AB75-0EDDDC680D2C",
                                "country": "IT",
                                "language": "it",
                                "order": 1,
                                "typeDescription": "Altre emissioni",
                                "subTypeDescription": "-"
                            }
                        }
                    },
                    {
                        "_id": "FC3F4BCB-D7E0-43CB-95A6-EE889067D030",
                        "code": "ENGINE",
                        "description": "Engine",
                        "typeCode": "ENG_BLANK",
                        "typeDescription": "",
                        "name": "Hybrid combined output (kW)",
                        "unitOfMeasure": "kW",
                        "values": [
                            {
                                "_id": "3D1714AE-378D-4CC7-904C-754BB9DE208E",
                                "value": "145",
                                "validFrom": "2023-03-01",
                                "validTo": "2999-12-01",
                                "final": None,
                                "languages": {},
                                "translations": {}
                            }
                        ],
                        "languages": {
                            "translations": [
                                "it-IT"
                            ],
                            "types": [
                                "it-IT"
                            ]
                        },
                        "translations": {
                            "it-IT": {
                                "_id": "B636C98A-C325-473E-ACB8-E04FDE893FBC",
                                "country": "IT",
                                "language": "it",
                                "order": 105,
                                "shortDescription": "Hybrid Synergy Drive: potenza massima kW",
                                "longDescription": "Hybrid Synergy Drive: potenza massima",
                                "marketingComment": None,
                                "highlight": False
                            }
                        },
                        "unitOfMeasureTranslations": {},
                        "types": {
                            "it-IT": {
                                "_id": "94E07105-4196-4D9E-85F1-BC2C93FAC7F1",
                                "country": "IT",
                                "language": "it",
                                "order": 9,
                                "typeDescription": "Motore",
                                "subTypeDescription": "-"
                            }
                        }
                    },
                    {
                        "_id": "9039F2B9-E0AE-41BF-A5B1-5C7C92ACAB48",
                        "code": "ENGINE",
                        "description": "Engine",
                        "typeCode": "ENG_BLANK",
                        "typeDescription": "",
                        "name": "Engine Code",
                        "unitOfMeasure": "",
                        "values": [
                            {
                                "_id": "AB55C0D1-89FE-4773-80C6-75F3002487C9",
                                "value": "M20A-FXS",
                                "validFrom": "2023-03-01",
                                "validTo": "2999-12-01",
                                "final": None,
                                "languages": {},
                                "translations": {}
                            }
                        ],
                        "languages": {
                            "types": [
                                "it-IT"
                            ]
                        },
                        "translations": {},
                        "unitOfMeasureTranslations": {},
                        "types": {
                            "it-IT": {
                                "_id": "94E07105-4196-4D9E-85F1-BC2C93FAC7F1",
                                "country": "IT",
                                "language": "it",
                                "order": 9,
                                "typeDescription": "Motore",
                                "subTypeDescription": "-"
                            }
                        }
                    },
                    {
                        "_id": "D679A18A-C438-490A-8A5A-37651DA1A742",
                        "code": "HYBRID_SYS",
                        "description": "Hybrid System",
                        "typeCode": "HYB_SYSBAT",
                        "typeDescription": "Hybrid system battery",
                        "name": "Capacity",
                        "unitOfMeasure": "Ah",
                        "values": [
                            {
                                "_id": "E3CD4BE4-4F49-48E7-88B3-79671A56B3F5",
                                "value": "4.08",
                                "validFrom": "2023-03-01",
                                "validTo": "2999-12-01",
                                "final": None,
                                "languages": {},
                                "translations": {}
                            }
                        ],
                        "languages": {
                            "translations": [
                                "it-IT"
                            ],
                            "types": [
                                "it-IT"
                            ]
                        },
                        "translations": {
                            "it-IT": {
                                "_id": "08E42DE3-77FC-485B-88EA-AFF8ABCE38E0",
                                "country": "IT",
                                "language": "it",
                                "order": 109,
                                "shortDescription": "Batterie HV: capacità",
                                "longDescription": "Batterie HV: capacità",
                                "marketingComment": None,
                                "highlight": False
                            }
                        },
                        "unitOfMeasureTranslations": {},
                        "types": {
                            "it-IT": {
                                "_id": "54C1C52D-8F35-49AB-B5F5-CDE47DCEF46D",
                                "country": "IT",
                                "language": "it",
                                "order": 13,
                                "typeDescription": "Sistema Ibrido / Sistema Fuel Cell",
                                "subTypeDescription": "-"
                            }
                        }
                    },
                    {
                        "_id": "694DD188-32CA-4A0C-9E6A-42E208CC4272",
                        "code": "INT_DIM",
                        "description": "Interior Dimensions",
                        "typeCode": "INT_BLANK",
                        "typeDescription": "",
                        "name": "Headroom (front)",
                        "unitOfMeasure": "mm",
                        "values": [
                            {
                                "_id": "0D27075C-7D95-4F83-A81E-7A09097F4A6E",
                                "value": "51",
                                "validFrom": "2023-03-01",
                                "validTo": "2999-12-01",
                                "final": None,
                                "languages": {},
                                "translations": {}
                            }
                        ],
                        "languages": {
                            "types": [
                                "it-IT"
                            ]
                        },
                        "translations": {},
                        "unitOfMeasureTranslations": {},
                        "types": {
                            "it-IT": {
                                "_id": "73B07E47-489B-435E-B6A1-D1D814FB2434",
                                "country": "IT",
                                "language": "it",
                                "order": 5,
                                "typeDescription": "Dimensioni interne",
                                "subTypeDescription": "-"
                            }
                        }
                    },
                    {
                        "_id": "D12DFC9E-55E4-48AE-AE76-F66AE03EF644",
                        "code": "ENGINE",
                        "description": "Engine",
                        "typeCode": "ENG_BLANK",
                        "typeDescription": "",
                        "name": "Hybrid combined output (hp)",
                        "unitOfMeasure": "DIN hp",
                        "values": [
                            {
                                "_id": "76D25415-76F6-41B7-B483-7F7C81A4FBD9",
                                "value": "197",
                                "validFrom": "2023-03-01",
                                "validTo": "2999-12-01",
                                "final": None,
                                "languages": {},
                                "translations": {}
                            }
                        ],
                        "languages": {
                            "translations": [
                                "it-IT"
                            ],
                            "types": [
                                "it-IT"
                            ]
                        },
                        "translations": {
                            "it-IT": {
                                "_id": "7582BB57-F2B5-44B1-9FF3-350CFC604AB2",
                                "country": "IT",
                                "language": "it",
                                "order": 104,
                                "shortDescription": "Hybrid Synergy Drive: potenza massima CV",
                                "longDescription": "Hybrid Synergy Drive: potenza massima",
                                "marketingComment": None,
                                "highlight": False
                            }
                        },
                        "unitOfMeasureTranslations": {},
                        "types": {
                            "it-IT": {
                                "_id": "94E07105-4196-4D9E-85F1-BC2C93FAC7F1",
                                "country": "IT",
                                "language": "it",
                                "order": 9,
                                "typeDescription": "Motore",
                                "subTypeDescription": "-"
                            }
                        }
                    },
                    {
                        "_id": "7EE139CB-C224-452F-ABE2-02780246FE3B",
                        "code": "INT_DIM",
                        "description": "Interior Dimensions",
                        "typeCode": "INT_BLANK",
                        "typeDescription": "",
                        "name": "Number of seating positions",
                        "unitOfMeasure": "",
                        "values": [
                            {
                                "_id": "7E0309F0-F952-4770-9D4C-83149300D978",
                                "value": "Anteriori 2, Posteriori 3",
                                "validFrom": "2023-03-01",
                                "validTo": "2999-12-01",
                                "final": None,
                                "languages": {},
                                "translations": {}
                            }
                        ],
                        "languages": {
                            "types": [
                                "it-IT"
                            ]
                        },
                        "translations": {},
                        "unitOfMeasureTranslations": {},
                        "types": {
                            "it-IT": {
                                "_id": "73B07E47-489B-435E-B6A1-D1D814FB2434",
                                "country": "IT",
                                "language": "it",
                                "order": 5,
                                "typeDescription": "Dimensioni interne",
                                "subTypeDescription": "-"
                            }
                        }
                    },
                    {
                        "_id": "77F043D4-A786-4C1A-BDC5-4ADC173A0F36",
                        "code": "HYBRID_SYS",
                        "description": "Hybrid System",
                        "typeCode": "HYB_ELECMO",
                        "typeDescription": "Electric motor",
                        "name": "Maximum torque",
                        "unitOfMeasure": "Nm",
                        "values": [
                            {
                                "_id": "25CE4C9B-731E-4F9E-B8EA-83CD51E46947",
                                "value": "206",
                                "validFrom": "2023-03-01",
                                "validTo": "2999-12-01",
                                "final": None,
                                "languages": {},
                                "translations": {}
                            }
                        ],
                        "languages": {
                            "types": [
                                "it-IT"
                            ]
                        },
                        "translations": {},
                        "unitOfMeasureTranslations": {},
                        "types": {
                            "it-IT": {
                                "_id": "54C1C52D-8F35-49AB-B5F5-CDE47DCEF46D",
                                "country": "IT",
                                "language": "it",
                                "order": 13,
                                "typeDescription": "Sistema Ibrido / Sistema Fuel Cell",
                                "subTypeDescription": "-"
                            }
                        }
                    },
                    {
                        "_id": "28B6879B-D985-4D94-A56C-904FFE195BBD",
                        "code": "SUSPENSION",
                        "description": "Suspension",
                        "typeCode": "SUS_BLANK",
                        "typeDescription": "",
                        "name": "Rear Suspension",
                        "unitOfMeasure": "",
                        "values": [
                            {
                                "_id": "1D1B82A7-50AD-4EC3-B9E6-83CD646F4F9F",
                                "value": "Doppio braccio oscillante",
                                "validFrom": "2023-03-01",
                                "validTo": "2999-12-01",
                                "final": None,
                                "languages": {},
                                "translations": {}
                            }
                        ],
                        "languages": {
                            "translations": [
                                "it-IT"
                            ],
                            "types": [
                                "it-IT"
                            ]
                        },
                        "translations": {
                            "it-IT": {
                                "_id": "6F5428A1-8813-45B5-A9E6-780A0830CB1B",
                                "country": "IT",
                                "language": "it",
                                "order": 143,
                                "shortDescription": "Sospensioni posteriori",
                                "longDescription": "Sospensioni posteriori",
                                "marketingComment": None,
                                "highlight": False
                            }
                        },
                        "unitOfMeasureTranslations": {},
                        "types": {
                            "it-IT": {
                                "_id": "BF7A6902-C9C9-4586-B97F-48621CE05BDC",
                                "country": "IT",
                                "language": "it",
                                "order": 14,
                                "typeDescription": "Sospensioni",
                                "subTypeDescription": "-"
                            }
                        }
                    },
                    {
                        "_id": "4135F9A6-D22A-4F23-9746-31F5A8C7D94F",
                        "code": "ENGINE",
                        "description": "Engine",
                        "typeCode": "ENG_BLANK",
                        "typeDescription": "",
                        "name": "Maximum output (kW)",
                        "unitOfMeasure": "kW",
                        "values": [
                            {
                                "_id": "2B7B5C18-92D7-4333-8191-8552DD9ABD73",
                                "value": "112",
                                "validFrom": "2023-03-01",
                                "validTo": "2999-12-01",
                                "final": None,
                                "languages": {},
                                "translations": {}
                            }
                        ],
                        "languages": {
                            "translations": [
                                "it-IT"
                            ],
                            "types": [
                                "it-IT"
                            ]
                        },
                        "translations": {
                            "it-IT": {
                                "_id": "669FD097-F020-4C77-8510-30F19857BA50",
                                "country": "IT",
                                "language": "it",
                                "order": 107,
                                "shortDescription": "Potenza max kW",
                                "longDescription": "Potenza max",
                                "marketingComment": None,
                                "highlight": False
                            }
                        },
                        "unitOfMeasureTranslations": {},
                        "types": {
                            "it-IT": {
                                "_id": "94E07105-4196-4D9E-85F1-BC2C93FAC7F1",
                                "country": "IT",
                                "language": "it",
                                "order": 9,
                                "typeDescription": "Motore",
                                "subTypeDescription": "-"
                            }
                        }
                    },
                    {
                        "_id": "EF1CEBDB-FC99-4C27-849E-49A56B613012",
                        "code": "WEIGHT",
                        "description": "Weight",
                        "typeCode": "WEIG_KERB",
                        "typeDescription": "Kerb weight",
                        "name": "In running order min",
                        "unitOfMeasure": "kg",
                        "values": [
                            {
                                "_id": "C7FA7904-1246-4241-B7D1-89F17DF6B83C",
                                "value": "1520",
                                "validFrom": "2023-03-01",
                                "validTo": "2999-12-01",
                                "final": None,
                                "languages": {},
                                "translations": {}
                            }
                        ],
                        "languages": {
                            "types": [
                                "it-IT"
                            ]
                        },
                        "translations": {},
                        "unitOfMeasureTranslations": {},
                        "types": {
                            "it-IT": {
                                "_id": "8D8FF346-3DB1-4222-9B51-53CAF38B83D6",
                                "country": "IT",
                                "language": "it",
                                "order": 10,
                                "typeDescription": "Pesi",
                                "subTypeDescription": "-"
                            }
                        }
                    },
                    {
                        "_id": "85C90CFE-2107-43DC-A347-0A3896CA49D3",
                        "code": "LUGGAGE",
                        "description": "Luggage Compartment",
                        "typeCode": "LUGG_BLANK",
                        "typeDescription": "",
                        "name": "VDA capacity up to tonneau cover (1st row up)",
                        "unitOfMeasure": "l",
                        "values": [
                            {
                                "_id": "10A5E216-9C0D-4A9F-BE65-8ECB0ABCAB64",
                                "value": "915",
                                "validFrom": "2023-03-01",
                                "validTo": "2999-12-01",
                                "final": None,
                                "languages": {},
                                "translations": {}
                            }
                        ],
                        "languages": {
                            "types": [
                                "it-IT"
                            ]
                        },
                        "translations": {},
                        "unitOfMeasureTranslations": {},
                        "types": {
                            "it-IT": {
                                "_id": "F344B59E-6151-4C65-9369-26936453B37B",
                                "country": "IT",
                                "language": "it",
                                "order": 2,
                                "typeDescription": "Bagagliaio",
                                "subTypeDescription": "-"
                            }
                        }
                    },
                    {
                        "_id": "5719956E-FFBC-462D-B454-5D50723103F5",
                        "code": "EXT_DIM",
                        "description": "Exterior Dimensions",
                        "typeCode": "EXT_BLANK",
                        "typeDescription": "",
                        "name": "Wheelbase",
                        "unitOfMeasure": "mm",
                        "values": [
                            {
                                "_id": "EA75B9A3-60DB-4C05-8CC4-905F569EEEB2",
                                "value": "2640",
                                "validFrom": "2023-03-01",
                                "validTo": "2999-12-01",
                                "final": None,
                                "languages": {},
                                "translations": {}
                            }
                        ],
                        "languages": {
                            "translations": [
                                "it-IT"
                            ],
                            "types": [
                                "it-IT"
                            ]
                        },
                        "translations": {
                            "it-IT": {
                                "_id": "4D754CD0-E5FB-4625-8490-5034099662E3",
                                "country": "IT",
                                "language": "it",
                                "order": 176,
                                "shortDescription": "Passo",
                                "longDescription": "Passo",
                                "marketingComment": None,
                                "highlight": False
                            }
                        },
                        "unitOfMeasureTranslations": {},
                        "types": {
                            "it-IT": {
                                "_id": "4F2D6E50-BC41-4A23-8426-833ECE779974",
                                "country": "IT",
                                "language": "it",
                                "order": 4,
                                "typeDescription": "Dimensioni esterne",
                                "subTypeDescription": "-"
                            }
                        }
                    },
                    {
                        "_id": "CCBCD443-D9CA-4D9D-B8B7-8CD8160683A5",
                        "code": "ENGINE",
                        "description": "Engine",
                        "typeCode": "ENG_BLANK",
                        "typeDescription": "",
                        "name": "RPM for max output",
                        "unitOfMeasure": "rpm",
                        "values": [
                            {
                                "_id": "CCC93E1B-F2B6-43BD-AAFE-949CA3D5C301",
                                "value": "6000",
                                "validFrom": "2023-03-01",
                                "validTo": "2999-12-01",
                                "final": None,
                                "languages": {},
                                "translations": {}
                            }
                        ],
                        "languages": {
                            "types": [
                                "it-IT"
                            ]
                        },
                        "translations": {},
                        "unitOfMeasureTranslations": {},
                        "types": {
                            "it-IT": {
                                "_id": "94E07105-4196-4D9E-85F1-BC2C93FAC7F1",
                                "country": "IT",
                                "language": "it",
                                "order": 9,
                                "typeDescription": "Motore",
                                "subTypeDescription": "-"
                            }
                        }
                    },
                    {
                        "_id": "5DB45B6A-C95B-493D-9D11-35FD592C05CB",
                        "code": "SUSPENSION",
                        "description": "Suspension",
                        "typeCode": "SUS_BLANK",
                        "typeDescription": "",
                        "name": "Rear Axle Track",
                        "unitOfMeasure": "mm",
                        "values": [
                            {
                                "_id": "C0C16FBA-DF2A-4434-BA59-96B71CEDE43D",
                                "value": "1560",
                                "validFrom": "2023-03-01",
                                "validTo": "2999-12-01",
                                "final": None,
                                "languages": {},
                                "translations": {}
                            }
                        ],
                        "languages": {
                            "types": [
                                "it-IT"
                            ]
                        },
                        "translations": {},
                        "unitOfMeasureTranslations": {},
                        "types": {
                            "it-IT": {
                                "_id": "BF7A6902-C9C9-4586-B97F-48621CE05BDC",
                                "country": "IT",
                                "language": "it",
                                "order": 14,
                                "typeDescription": "Sospensioni",
                                "subTypeDescription": "-"
                            }
                        }
                    },
                    {
                        "_id": "40AE71DE-A2D4-43A4-A690-B7506A5668F1",
                        "code": "EXT_DIM",
                        "description": "Exterior Dimensions",
                        "typeCode": "EXT_BLANK",
                        "typeDescription": "",
                        "name": "Departure angle",
                        "unitOfMeasure": "0",
                        "values": [
                            {
                                "_id": "FDE89F22-943B-46FF-8378-96C76862F51F",
                                "value": "28.5",
                                "validFrom": "2023-03-01",
                                "validTo": "2999-12-01",
                                "final": None,
                                "languages": {},
                                "translations": {}
                            }
                        ],
                        "languages": {
                            "translations": [
                                "it-IT"
                            ],
                            "types": [
                                "it-IT"
                            ]
                        },
                        "translations": {
                            "it-IT": {
                                "_id": "BB912BE2-5C3A-4E39-B2DD-AA0832115260",
                                "country": "IT",
                                "language": "it",
                                "order": 161,
                                "shortDescription": "Angolo di uscita",
                                "longDescription": "Angolo di uscita",
                                "marketingComment": None,
                                "highlight": False
                            }
                        },
                        "unitOfMeasureTranslations": {},
                        "types": {
                            "it-IT": {
                                "_id": "4F2D6E50-BC41-4A23-8426-833ECE779974",
                                "country": "IT",
                                "language": "it",
                                "order": 4,
                                "typeDescription": "Dimensioni esterne",
                                "subTypeDescription": "-"
                            }
                        }
                    },
                    {
                        "_id": "1DA4E0D6-7A79-4DBD-B10D-D879E6463338",
                        "code": "CO2_EMIS",
                        "description": "CO2 Emissions",
                        "typeCode": "CO2_BLANK",
                        "typeDescription": "",
                        "name": "Combined",
                        "unitOfMeasure": "g/km",
                        "values": [
                            {
                                "_id": "BE9A08C9-E15F-4232-A0BA-A08BEEF030BA",
                                "value": "112.6",
                                "validFrom": "2023-03-01",
                                "validTo": "2999-12-01",
                                "final": None,
                                "languages": {},
                                "translations": {}
                            }
                        ],
                        "languages": {
                            "translations": [
                                "it-IT"
                            ],
                            "types": [
                                "it-IT"
                            ]
                        },
                        "translations": {
                            "it-IT": {
                                "_id": "4FF2E63C-C637-40A6-ADC3-14FDA5A3955C",
                                "country": "IT",
                                "language": "it",
                                "order": 101,
                                "shortDescription": "Emissioni CO2",
                                "longDescription": "Emissioni CO2",
                                "marketingComment": None,
                                "highlight": False
                            }
                        },
                        "unitOfMeasureTranslations": {},
                        "types": {
                            "it-IT": {
                                "_id": "44C8BE0B-3A70-40C9-B723-C78F2CE4096C",
                                "country": "IT",
                                "language": "it",
                                "order": 6,
                                "typeDescription": "Emissioni",
                                "subTypeDescription": "-"
                            }
                        }
                    },
                    {
                        "_id": "E5EE3EB2-0C9D-4784-9630-87FEC4478155",
                        "code": "EXT_DIM",
                        "description": "Exterior Dimensions",
                        "typeCode": "EXT_BLANK",
                        "typeDescription": "",
                        "name": "Overhang (front)",
                        "unitOfMeasure": "mm",
                        "values": [
                            {
                                "_id": "9EB3023F-3770-4EF9-A9D7-A3F8326609ED",
                                "value": "955",
                                "validFrom": "2023-03-01",
                                "validTo": "2999-12-01",
                                "final": None,
                                "languages": {},
                                "translations": {}
                            }
                        ],
                        "languages": {
                            "translations": [
                                "it-IT"
                            ],
                            "types": [
                                "it-IT"
                            ]
                        },
                        "translations": {
                            "it-IT": {
                                "_id": "035F51B1-64D7-4678-A6E9-E1D2BC446077",
                                "country": "IT",
                                "language": "it",
                                "order": 171,
                                "shortDescription": "Sbalzo anteriore",
                                "longDescription": "Sbalzo anteriore",
                                "marketingComment": None,
                                "highlight": False
                            }
                        },
                        "unitOfMeasureTranslations": {},
                        "types": {
                            "it-IT": {
                                "_id": "4F2D6E50-BC41-4A23-8426-833ECE779974",
                                "country": "IT",
                                "language": "it",
                                "order": 4,
                                "typeDescription": "Dimensioni esterne",
                                "subTypeDescription": "-"
                            }
                        }
                    },
                    {
                        "_id": "12ECEDDA-750F-4962-938F-D3A549D40534",
                        "code": "STEERING",
                        "description": "Steering",
                        "typeCode": "STEE_BLANK",
                        "typeDescription": "",
                        "name": "Minimum turning radius (tyres)",
                        "unitOfMeasure": "m",
                        "values": [
                            {
                                "_id": "A5EE1EC3-D55A-494D-A1C1-A8ABF036AD67",
                                "value": "5.2",
                                "validFrom": "2023-03-01",
                                "validTo": "2999-12-01",
                                "final": None,
                                "languages": {},
                                "translations": {}
                            }
                        ],
                        "languages": {
                            "translations": [
                                "it-IT"
                            ],
                            "types": [
                                "it-IT"
                            ]
                        },
                        "translations": {
                            "it-IT": {
                                "_id": "75308130-FAA4-4F38-AF95-7A16115A9C7D",
                                "country": "IT",
                                "language": "it",
                                "order": 146,
                                "shortDescription": "Raggio di sterzata ruote",
                                "longDescription": "Raggio di sterzata",
                                "marketingComment": None,
                                "highlight": False
                            }
                        },
                        "unitOfMeasureTranslations": {},
                        "types": {
                            "it-IT": {
                                "_id": "A1DF6115-09EA-4431-9B25-6BB5ACB84416",
                                "country": "IT",
                                "language": "it",
                                "order": 15,
                                "typeDescription": "Sterzo",
                                "subTypeDescription": "-"
                            }
                        }
                    },
                    {
                        "_id": "9D9C6297-DA96-4075-92E3-C482F5B9DB15",
                        "code": "ENGINE",
                        "description": "Engine",
                        "typeCode": "ENG_BLANK",
                        "typeDescription": "",
                        "name": "Bore",
                        "unitOfMeasure": "mm",
                        "values": [
                            {
                                "_id": "2567B79F-DAC0-4AB3-A5B1-ABE94DA20115",
                                "value": "80.5",
                                "validFrom": "2023-03-01",
                                "validTo": "2999-12-01",
                                "final": None,
                                "languages": {},
                                "translations": {}
                            }
                        ],
                        "languages": {
                            "translations": [
                                "it-IT"
                            ],
                            "types": [
                                "it-IT"
                            ]
                        },
                        "translations": {
                            "it-IT": {
                                "_id": "47F1DF4B-D534-427D-B3F5-1BB619645F83",
                                "country": "IT",
                                "language": "it",
                                "order": 114,
                                "shortDescription": "Alesaggio x corsa",
                                "longDescription": "Alesaggio x corsa",
                                "marketingComment": None,
                                "highlight": False
                            }
                        },
                        "unitOfMeasureTranslations": {},
                        "types": {
                            "it-IT": {
                                "_id": "94E07105-4196-4D9E-85F1-BC2C93FAC7F1",
                                "country": "IT",
                                "language": "it",
                                "order": 9,
                                "typeDescription": "Motore",
                                "subTypeDescription": "-"
                            }
                        }
                    },
                    {
                        "_id": "61C9A4A3-AC62-4A34-BFF0-3C7D847377C1",
                        "code": "CO2_EMIS",
                        "description": "CO2 Emissions",
                        "typeCode": "CO2_BLANK",
                        "typeDescription": "",
                        "name": "Urban",
                        "unitOfMeasure": "g/km",
                        "values": [
                            {
                                "_id": "007AE64B-1529-4978-91BE-AED0E0E06402",
                                "value": "119.9",
                                "validFrom": "2023-03-01",
                                "validTo": "2999-12-01",
                                "final": None,
                                "languages": {},
                                "translations": {}
                            }
                        ],
                        "languages": {
                            "types": [
                                "it-IT"
                            ]
                        },
                        "translations": {},
                        "unitOfMeasureTranslations": {},
                        "types": {
                            "it-IT": {
                                "_id": "44C8BE0B-3A70-40C9-B723-C78F2CE4096C",
                                "country": "IT",
                                "language": "it",
                                "order": 6,
                                "typeDescription": "Emissioni",
                                "subTypeDescription": "-"
                            }
                        }
                    },
                    {
                        "_id": "11FCCE71-134A-41D5-918F-99A0F523AB1B",
                        "code": "NOISE",
                        "description": "Noise Levels",
                        "typeCode": "NOI_BLANK",
                        "typeDescription": "",
                        "name": "Engine speed for stationary noise",
                        "unitOfMeasure": "1/min",
                        "values": [
                            {
                                "_id": "627D68B4-90CD-4437-9D1E-B4604B9BDFAE",
                                "value": "2500",
                                "validFrom": "2023-03-01",
                                "validTo": "2999-12-01",
                                "final": None,
                                "languages": {},
                                "translations": {}
                            }
                        ],
                        "languages": {
                            "types": [
                                "it-IT"
                            ]
                        },
                        "translations": {},
                        "unitOfMeasureTranslations": {},
                        "types": {
                            "it-IT": {
                                "_id": "CDA5F573-948C-43C6-86C9-90CC22DD4DF2",
                                "country": "IT",
                                "language": "it",
                                "order": 7,
                                "typeDescription": "Emissioni acustiche",
                                "subTypeDescription": "-"
                            }
                        }
                    },
                    {
                        "_id": "BD2E0461-DDAD-4930-8AEA-63AAFFD92FE6",
                        "code": "LUGGAGE",
                        "description": "Luggage Compartment",
                        "typeCode": "LUGG_BLANK",
                        "typeDescription": "",
                        "name": "Luggage room length (1st & 2nd rows up)",
                        "unitOfMeasure": "",
                        "values": [
                            {
                                "_id": "D3DBB133-E092-4CF5-AFE6-B6AF48F34D85",
                                "value": "835",
                                "validFrom": "2023-03-01",
                                "validTo": "2999-12-01",
                                "final": None,
                                "languages": {},
                                "translations": {}
                            }
                        ],
                        "languages": {
                            "types": [
                                "it-IT"
                            ]
                        },
                        "translations": {},
                        "unitOfMeasureTranslations": {},
                        "types": {
                            "it-IT": {
                                "_id": "F344B59E-6151-4C65-9369-26936453B37B",
                                "country": "IT",
                                "language": "it",
                                "order": 2,
                                "typeDescription": "Bagagliaio",
                                "subTypeDescription": "-"
                            }
                        }
                    },
                    {
                        "_id": "4ACD2B6B-233E-46E8-AD63-9CDC16FF5297",
                        "code": "OTHER_EMIS",
                        "description": "Other Emissions",
                        "typeCode": "OTH_BLANK",
                        "typeDescription": "",
                        "name": "Exhaust Emissions EC Reg (Base)",
                        "unitOfMeasure": "",
                        "values": [
                            {
                                "_id": "551842E0-A7CA-417A-850C-B6B8A8B2A397",
                                "value": "715/2007",
                                "validFrom": "2023-03-01",
                                "validTo": "2999-12-01",
                                "final": None,
                                "languages": {},
                                "translations": {}
                            }
                        ],
                        "languages": {
                            "types": [
                                "it-IT"
                            ]
                        },
                        "translations": {},
                        "unitOfMeasureTranslations": {},
                        "types": {
                            "it-IT": {
                                "_id": "5AF52DD9-0DB5-477E-AB75-0EDDDC680D2C",
                                "country": "IT",
                                "language": "it",
                                "order": 1,
                                "typeDescription": "Altre emissioni",
                                "subTypeDescription": "-"
                            }
                        }
                    },
                    {
                        "_id": "60AD65B4-5573-4D0B-B998-2202650B6CF4",
                        "code": "OTHER_EMIS",
                        "description": "Other Emissions",
                        "typeCode": "OTH_BLANK",
                        "typeDescription": "",
                        "name": "Hydrocarbons (THC)",
                        "unitOfMeasure": "mg/km",
                        "values": [
                            {
                                "_id": "75AEB274-A658-466D-AFC5-B84EC1F5105F",
                                "value": "19.2",
                                "validFrom": "2023-03-01",
                                "validTo": "2999-12-01",
                                "final": None,
                                "languages": {},
                                "translations": {}
                            }
                        ],
                        "languages": {
                            "types": [
                                "it-IT"
                            ]
                        },
                        "translations": {},
                        "unitOfMeasureTranslations": {},
                        "types": {
                            "it-IT": {
                                "_id": "5AF52DD9-0DB5-477E-AB75-0EDDDC680D2C",
                                "country": "IT",
                                "language": "it",
                                "order": 1,
                                "typeDescription": "Altre emissioni",
                                "subTypeDescription": "-"
                            }
                        }
                    },
                    {
                        "_id": "456D1844-8624-4ACE-96B8-55423710131F",
                        "code": "TRANSMIS",
                        "description": "Transmission",
                        "typeCode": "TR_BLANK",
                        "typeDescription": "",
                        "name": "Differerential gear ratio",
                        "unitOfMeasure": "",
                        "values": [
                            {
                                "_id": "EC6D42C7-C75F-4905-94E9-BC5820050696",
                                "value": "3.605",
                                "validFrom": "2023-03-01",
                                "validTo": "2999-12-01",
                                "final": None,
                                "languages": {},
                                "translations": {}
                            }
                        ],
                        "languages": {
                            "types": [
                                "it-IT"
                            ]
                        },
                        "translations": {},
                        "unitOfMeasureTranslations": {},
                        "types": {
                            "it-IT": {
                                "_id": "25341A56-E0E6-461E-A387-6A879969708D",
                                "country": "IT",
                                "language": "it",
                                "order": 16,
                                "typeDescription": "Trasmissione",
                                "subTypeDescription": "-"
                            }
                        }
                    },
                    {
                        "_id": "B110E71A-65E0-4013-9651-EF16AF505DA5",
                        "code": "BRAKES",
                        "description": "Brakes",
                        "typeCode": "BRAK_BLANK",
                        "typeDescription": "",
                        "name": "Brake type rear",
                        "unitOfMeasure": "",
                        "values": [
                            {
                                "_id": "44D54A6C-F50A-469A-998A-BE71C58499E7",
                                "value": "Disco",
                                "validFrom": "2023-03-01",
                                "validTo": "2999-12-01",
                                "final": None,
                                "languages": {},
                                "translations": {}
                            }
                        ],
                        "languages": {
                            "translations": [
                                "it-IT"
                            ],
                            "types": [
                                "it-IT"
                            ]
                        },
                        "translations": {
                            "it-IT": {
                                "_id": "FABC4D13-DE77-4A4D-823B-4EA6C88B3CF1",
                                "country": "IT",
                                "language": "it",
                                "order": 145,
                                "shortDescription": "Freni posteriori",
                                "longDescription": "Freni posteriori",
                                "marketingComment": None,
                                "highlight": False
                            }
                        },
                        "unitOfMeasureTranslations": {},
                        "types": {
                            "it-IT": {
                                "_id": "163D3D94-8B08-488C-AE79-1BF872DE08CE",
                                "country": "IT",
                                "language": "it",
                                "order": 8,
                                "typeDescription": "Freni",
                                "subTypeDescription": "-"
                            }
                        }
                    },
                    {
                        "_id": "C0BF1CAE-A22E-49D7-8F13-6EEDB9F22EE6",
                        "code": "NOISE",
                        "description": "Noise Levels",
                        "typeCode": "NOI_BLANK",
                        "typeDescription": "",
                        "name": "Stationary noise",
                        "unitOfMeasure": "dB(A)",
                        "values": [
                            {
                                "_id": "17A06B43-6EF0-4BB7-8C31-C2309F1D4DBB",
                                "value": "67.0",
                                "validFrom": "2023-03-01",
                                "validTo": "2999-12-01",
                                "final": None,
                                "languages": {},
                                "translations": {}
                            }
                        ],
                        "languages": {
                            "translations": [
                                "it-IT"
                            ],
                            "types": [
                                "it-IT"
                            ]
                        },
                        "translations": {
                            "it-IT": {
                                "_id": "2C4A4240-6162-4774-B094-9D3924431514",
                                "country": "IT",
                                "language": "it",
                                "order": 184,
                                "shortDescription": "Livello sonoro a veicolo fermo",
                                "longDescription": "Livello sonoro a veicolo fermo",
                                "marketingComment": None,
                                "highlight": False
                            }
                        },
                        "unitOfMeasureTranslations": {},
                        "types": {
                            "it-IT": {
                                "_id": "CDA5F573-948C-43C6-86C9-90CC22DD4DF2",
                                "country": "IT",
                                "language": "it",
                                "order": 7,
                                "typeDescription": "Emissioni acustiche",
                                "subTypeDescription": "-"
                            }
                        }
                    },
                    {
                        "_id": "F7C87F62-540D-45C9-91AE-BD1B9F71B554",
                        "code": "NOISE",
                        "description": "Noise Levels",
                        "typeCode": "NOI_BLANK",
                        "typeDescription": "",
                        "name": "Drive-by noise",
                        "unitOfMeasure": "dB(A)",
                        "values": [
                            {
                                "_id": "61EF2756-4FC9-4D11-9B7C-C2B8FCAD7FF6",
                                "value": "66.0",
                                "validFrom": "2023-03-01",
                                "validTo": "2999-12-01",
                                "final": None,
                                "languages": {},
                                "translations": {}
                            }
                        ],
                        "languages": {
                            "translations": [
                                "it-IT"
                            ],
                            "types": [
                                "it-IT"
                            ]
                        },
                        "translations": {
                            "it-IT": {
                                "_id": "C8D58573-458A-453C-A56A-6F837C7BB270",
                                "country": "IT",
                                "language": "it",
                                "order": 183,
                                "shortDescription": "Livello sonoro a veicolo in movimento",
                                "longDescription": "Livello sonoro a veicolo in movimento",
                                "marketingComment": None,
                                "highlight": False
                            }
                        },
                        "unitOfMeasureTranslations": {},
                        "types": {
                            "it-IT": {
                                "_id": "CDA5F573-948C-43C6-86C9-90CC22DD4DF2",
                                "country": "IT",
                                "language": "it",
                                "order": 7,
                                "typeDescription": "Emissioni acustiche",
                                "subTypeDescription": "-"
                            }
                        }
                    },
                    {
                        "_id": "94DB1087-8599-43B8-AFEA-71D1ACBD413E",
                        "code": "EXT_DIM",
                        "description": "Exterior Dimensions",
                        "typeCode": "EXT_BLANK",
                        "typeDescription": "",
                        "name": "Approach angle",
                        "unitOfMeasure": "0",
                        "values": [
                            {
                                "_id": "09163FB6-E3EE-49A8-9095-C4FCBE8B86E1",
                                "value": "16",
                                "validFrom": "2023-03-01",
                                "validTo": "2999-12-01",
                                "final": None,
                                "languages": {},
                                "translations": {}
                            }
                        ],
                        "languages": {
                            "translations": [
                                "it-IT"
                            ],
                            "types": [
                                "it-IT"
                            ]
                        },
                        "translations": {
                            "it-IT": {
                                "_id": "4B4C9427-B79F-4A1E-9BC5-EF71503BCA99",
                                "country": "IT",
                                "language": "it",
                                "order": 158,
                                "shortDescription": "Angolo di attacco",
                                "longDescription": "Angolo di attacco",
                                "marketingComment": None,
                                "highlight": False
                            }
                        },
                        "unitOfMeasureTranslations": {},
                        "types": {
                            "it-IT": {
                                "_id": "4F2D6E50-BC41-4A23-8426-833ECE779974",
                                "country": "IT",
                                "language": "it",
                                "order": 4,
                                "typeDescription": "Dimensioni esterne",
                                "subTypeDescription": "-"
                            }
                        }
                    },
                    {
                        "_id": "636FA632-D284-4C0E-9163-64FD080796C4",
                        "code": "FUEL_CONS",
                        "description": "Fuel Consumption",
                        "typeCode": "FUEL_BLANK",
                        "typeDescription": "",
                        "name": "Urban",
                        "unitOfMeasure": "l/100km",
                        "values": [
                            {
                                "_id": "2D65DDFD-7334-4DCB-AED4-C7CBE1F59DFE",
                                "value": "5.28",
                                "validFrom": "2023-03-01",
                                "validTo": "2999-12-01",
                                "final": None,
                                "languages": {},
                                "translations": {}
                            }
                        ],
                        "languages": {
                            "translations": [
                                "it-IT"
                            ],
                            "types": [
                                "it-IT"
                            ]
                        },
                        "translations": {
                            "it-IT": {
                                "_id": "52BBF5C1-6925-4CAD-A442-AA39E59A924A",
                                "country": "IT",
                                "language": "it",
                                "order": 138,
                                "shortDescription": "Urbano",
                                "longDescription": "Urbano",
                                "marketingComment": None,
                                "highlight": False
                            }
                        },
                        "unitOfMeasureTranslations": {},
                        "types": {
                            "it-IT": {
                                "_id": "A5023D92-7A67-4B22-AEF3-7D5CDCB0AE1A",
                                "country": "IT",
                                "language": "it",
                                "order": 3,
                                "typeDescription": "Consumi",
                                "subTypeDescription": "-"
                            }
                        }
                    },
                    {
                        "_id": "1885B0E8-14A0-4669-9CB8-80195555480F",
                        "code": "WEIGHT",
                        "description": "Weight",
                        "typeCode": "WEIG_KERB",
                        "typeDescription": "Kerb weight",
                        "name": "In running order max",
                        "unitOfMeasure": "kg",
                        "values": [
                            {
                                "_id": "B686BEE8-7395-40C3-8BED-CB258CC3EC69",
                                "value": "1580",
                                "validFrom": "2023-03-01",
                                "validTo": "2999-12-01",
                                "final": None,
                                "languages": {},
                                "translations": {}
                            }
                        ],
                        "languages": {
                            "types": [
                                "it-IT"
                            ]
                        },
                        "translations": {},
                        "unitOfMeasureTranslations": {},
                        "types": {
                            "it-IT": {
                                "_id": "8D8FF346-3DB1-4222-9B51-53CAF38B83D6",
                                "country": "IT",
                                "language": "it",
                                "order": 10,
                                "typeDescription": "Pesi",
                                "subTypeDescription": "-"
                            }
                        }
                    },
                    {
                        "_id": "80DB941B-9C5F-44E1-9348-59D726B1DF2A",
                        "code": "EXT_DIM",
                        "description": "Exterior Dimensions",
                        "typeCode": "EXT_BLANK",
                        "typeDescription": "",
                        "name": "Overall width",
                        "unitOfMeasure": "mm",
                        "values": [
                            {
                                "_id": "344A1825-714C-4115-8539-D24122AB4A8E",
                                "value": "1825",
                                "validFrom": "2023-03-01",
                                "validTo": "2999-12-01",
                                "final": None,
                                "languages": {},
                                "translations": {}
                            }
                        ],
                        "languages": {
                            "translations": [
                                "it-IT"
                            ],
                            "types": [
                                "it-IT"
                            ]
                        },
                        "translations": {
                            "it-IT": {
                                "_id": "043BF3E0-4BF4-49F2-BA4A-34BC1B0EBE0B",
                                "country": "IT",
                                "language": "it",
                                "order": 169,
                                "shortDescription": "Larghezza totale",
                                "longDescription": "Larghezza totale",
                                "marketingComment": None,
                                "highlight": False
                            }
                        },
                        "unitOfMeasureTranslations": {},
                        "types": {
                            "it-IT": {
                                "_id": "4F2D6E50-BC41-4A23-8426-833ECE779974",
                                "country": "IT",
                                "language": "it",
                                "order": 4,
                                "typeDescription": "Dimensioni esterne",
                                "subTypeDescription": "-"
                            }
                        }
                    },
                    {
                        "_id": "AEA9D46C-AF09-4B84-8BC8-5AAE30D6CF04",
                        "code": "CO2_EMIS",
                        "description": "CO2 Emissions",
                        "typeCode": "CO2_BLANK",
                        "typeDescription": "",
                        "name": "The type of test procedure",
                        "unitOfMeasure": "",
                        "values": [
                            {
                                "_id": "BF55369B-BD84-4C58-B961-D326C5BAE025",
                                "value": "TYPE I",
                                "validFrom": "2023-03-01",
                                "validTo": "2999-12-01",
                                "final": None,
                                "languages": {},
                                "translations": {}
                            }
                        ],
                        "languages": {
                            "types": [
                                "it-IT"
                            ]
                        },
                        "translations": {},
                        "unitOfMeasureTranslations": {},
                        "types": {
                            "it-IT": {
                                "_id": "44C8BE0B-3A70-40C9-B723-C78F2CE4096C",
                                "country": "IT",
                                "language": "it",
                                "order": 6,
                                "typeDescription": "Emissioni",
                                "subTypeDescription": "-"
                            }
                        }
                    },
                    {
                        "_id": "0D88FA72-6B26-4E7C-80D6-DA375428687F",
                        "code": "ENGINE",
                        "description": "Engine",
                        "typeCode": "ENG_BLANK",
                        "typeDescription": "",
                        "name": "Compression ratio",
                        "unitOfMeasure": "",
                        "values": [
                            {
                                "_id": "5D770B43-04C3-4DC5-B822-D4F9324F0FFB",
                                "value": "14:1",
                                "validFrom": "2023-03-01",
                                "validTo": "2999-12-01",
                                "final": None,
                                "languages": {},
                                "translations": {}
                            }
                        ],
                        "languages": {
                            "translations": [
                                "it-IT"
                            ],
                            "types": [
                                "it-IT"
                            ]
                        },
                        "translations": {
                            "it-IT": {
                                "_id": "F9FF3282-598A-483E-BA4A-581310D3667A",
                                "country": "IT",
                                "language": "it",
                                "order": 102,
                                "shortDescription": "Rapporto di compressione",
                                "longDescription": "Rapporto di compressione",
                                "marketingComment": None,
                                "highlight": False
                            }
                        },
                        "unitOfMeasureTranslations": {},
                        "types": {
                            "it-IT": {
                                "_id": "94E07105-4196-4D9E-85F1-BC2C93FAC7F1",
                                "country": "IT",
                                "language": "it",
                                "order": 9,
                                "typeDescription": "Motore",
                                "subTypeDescription": "-"
                            }
                        }
                    },
                    {
                        "_id": "B9C2D3B1-82D6-43EC-88BA-25EDFF3C5E14",
                        "code": "BRAKES",
                        "description": "Brakes",
                        "typeCode": "BRAK_BLANK",
                        "typeDescription": "",
                        "name": "Brake size rear",
                        "unitOfMeasure": "mm",
                        "values": [
                            {
                                "_id": "ABE44F78-4517-4E82-A5F7-D6B1008C8163",
                                "value": "16\" epb",
                                "validFrom": "2023-03-01",
                                "validTo": "2999-12-01",
                                "final": None,
                                "languages": {},
                                "translations": {}
                            }
                        ],
                        "languages": {
                            "translations": [
                                "it-IT"
                            ],
                            "types": [
                                "it-IT"
                            ]
                        },
                        "translations": {
                            "it-IT": {
                                "_id": "CCB8F537-FED1-4E55-96B0-C7D8F4FF0124",
                                "country": "IT",
                                "language": "it",
                                "order": 179,
                                "shortDescription": "Freni posteriori",
                                "longDescription": "Freni posteriori",
                                "marketingComment": None,
                                "highlight": False
                            }
                        },
                        "unitOfMeasureTranslations": {},
                        "types": {
                            "it-IT": {
                                "_id": "163D3D94-8B08-488C-AE79-1BF872DE08CE",
                                "country": "IT",
                                "language": "it",
                                "order": 8,
                                "typeDescription": "Freni",
                                "subTypeDescription": "-"
                            }
                        }
                    },
                    {
                        "_id": "8307834A-82B0-4524-B1BC-603DEE5635C8",
                        "code": "HYBRID_SYS",
                        "description": "Hybrid System",
                        "typeCode": "HYB_ELECMO",
                        "typeDescription": "Electric motor",
                        "name": "Maximum output (kW)",
                        "unitOfMeasure": "kW",
                        "values": [
                            {
                                "_id": "88AAAEB8-84A7-48FE-A229-D71623BA8EAA",
                                "value": "83",
                                "validFrom": "2023-03-01",
                                "validTo": "2999-12-01",
                                "final": None,
                                "languages": {},
                                "translations": {}
                            }
                        ],
                        "languages": {
                            "translations": [
                                "it-IT"
                            ],
                            "types": [
                                "it-IT"
                            ]
                        },
                        "translations": {
                            "it-IT": {
                                "_id": "4A7413A6-335F-4E39-A911-32B931CF9322",
                                "country": "IT",
                                "language": "it",
                                "order": 113,
                                "shortDescription": "Hybrid Sinergy Drive: potenza massima kW",
                                "longDescription": "Hybrid Sinergy Drive: potenza massima",
                                "marketingComment": None,
                                "highlight": False
                            }
                        },
                        "unitOfMeasureTranslations": {},
                        "types": {
                            "it-IT": {
                                "_id": "54C1C52D-8F35-49AB-B5F5-CDE47DCEF46D",
                                "country": "IT",
                                "language": "it",
                                "order": 13,
                                "typeDescription": "Sistema Ibrido / Sistema Fuel Cell",
                                "subTypeDescription": "-"
                            }
                        }
                    },
                    {
                        "_id": "F4D8F17A-0F36-4F23-9C5C-8F59099AF30B",
                        "code": "TRANSMIS",
                        "description": "Transmission",
                        "typeCode": "TR_BLANK",
                        "typeDescription": "",
                        "name": "Driven wheels",
                        "unitOfMeasure": "",
                        "values": [
                            {
                                "_id": "3D465B29-60D3-4DC0-9160-DB61657FA709",
                                "value": "FWD",
                                "validFrom": "2023-03-01",
                                "validTo": "2999-12-01",
                                "final": None,
                                "languages": {},
                                "translations": {}
                            }
                        ],
                        "languages": {
                            "translations": [
                                "it-IT"
                            ],
                            "types": [
                                "it-IT"
                            ]
                        },
                        "translations": {
                            "it-IT": {
                                "_id": "00E7E839-BB51-4204-A39D-1FB721084C98",
                                "country": "IT",
                                "language": "it",
                                "order": 130,
                                "shortDescription": "Trazione",
                                "longDescription": "Trazione",
                                "marketingComment": None,
                                "highlight": False
                            }
                        },
                        "unitOfMeasureTranslations": {},
                        "types": {
                            "it-IT": {
                                "_id": "25341A56-E0E6-461E-A387-6A879969708D",
                                "country": "IT",
                                "language": "it",
                                "order": 16,
                                "typeDescription": "Trasmissione",
                                "subTypeDescription": "-"
                            }
                        }
                    },
                    {
                        "_id": "B709454E-FF96-42A0-8F0E-9DB52FC50C82",
                        "code": "BRAKES",
                        "description": "Brakes",
                        "typeCode": "BRAK_BLANK",
                        "typeDescription": "",
                        "name": "Brake size front",
                        "unitOfMeasure": "mm",
                        "values": [
                            {
                                "_id": "75AFD295-9049-41B8-B910-DF7B0F58D1E7",
                                "value": "16\" disco",
                                "validFrom": "2023-03-01",
                                "validTo": "2999-12-01",
                                "final": None,
                                "languages": {},
                                "translations": {}
                            }
                        ],
                        "languages": {
                            "translations": [
                                "it-IT"
                            ],
                            "types": [
                                "it-IT"
                            ]
                        },
                        "translations": {
                            "it-IT": {
                                "_id": "019DC655-16B1-4993-8B37-2FBE96432396",
                                "country": "IT",
                                "language": "it",
                                "order": 178,
                                "shortDescription": "Freni anteriori",
                                "longDescription": "Freni anteriori",
                                "marketingComment": None,
                                "highlight": False
                            }
                        },
                        "unitOfMeasureTranslations": {},
                        "types": {
                            "it-IT": {
                                "_id": "163D3D94-8B08-488C-AE79-1BF872DE08CE",
                                "country": "IT",
                                "language": "it",
                                "order": 8,
                                "typeDescription": "Freni",
                                "subTypeDescription": "-"
                            }
                        }
                    },
                    {
                        "_id": "EA8D555A-1073-46F6-A05D-8D7EB61CF3BB",
                        "code": "HYBRID_SYS",
                        "description": "Hybrid System",
                        "typeCode": "HYB_ELECMO",
                        "typeDescription": "Electric motor",
                        "name": "Electric motor Type",
                        "unitOfMeasure": "",
                        "values": [
                            {
                                "_id": "6A851FF4-8F81-405A-B16A-E4029C9B7139",
                                "value": "Sincrono a magneti permanenti",
                                "validFrom": "2023-03-01",
                                "validTo": "2999-12-01",
                                "final": None,
                                "languages": {},
                                "translations": {}
                            }
                        ],
                        "languages": {
                            "translations": [
                                "it-IT"
                            ],
                            "types": [
                                "it-IT"
                            ]
                        },
                        "translations": {
                            "it-IT": {
                                "_id": "36831A5D-64DA-4724-AF5B-F178B6A34344",
                                "country": "IT",
                                "language": "it",
                                "order": 110,
                                "shortDescription": "Motore elettrico: tipo",
                                "longDescription": "Motore elettrico: tipo",
                                "marketingComment": None,
                                "highlight": False
                            }
                        },
                        "unitOfMeasureTranslations": {},
                        "types": {
                            "it-IT": {
                                "_id": "54C1C52D-8F35-49AB-B5F5-CDE47DCEF46D",
                                "country": "IT",
                                "language": "it",
                                "order": 13,
                                "typeDescription": "Sistema Ibrido / Sistema Fuel Cell",
                                "subTypeDescription": "-"
                            }
                        }
                    },
                    {
                        "_id": "078A884B-95BE-4098-8B37-9FCBD9515FDF",
                        "code": "OTHER_EMIS",
                        "description": "Other Emissions",
                        "typeCode": "OTH_BLANK",
                        "typeDescription": "",
                        "name": "Nitrogen Oxides (NOx)",
                        "unitOfMeasure": "mg/km",
                        "values": [
                            {
                                "_id": "7D627CD0-7794-4612-9F57-E6043F4B9AE1",
                                "value": "3.9",
                                "validFrom": "2023-03-01",
                                "validTo": "2999-12-01",
                                "final": None,
                                "languages": {},
                                "translations": {}
                            }
                        ],
                        "languages": {
                            "translations": [
                                "it-IT"
                            ],
                            "types": [
                                "it-IT"
                            ]
                        },
                        "translations": {
                            "it-IT": {
                                "_id": "91011AA8-2870-429B-B443-991EEE916EF3",
                                "country": "IT",
                                "language": "it",
                                "order": 182,
                                "shortDescription": "Emissioni NOx",
                                "longDescription": "Emissioni NOx",
                                "marketingComment": None,
                                "highlight": False
                            }
                        },
                        "unitOfMeasureTranslations": {},
                        "types": {
                            "it-IT": {
                                "_id": "5AF52DD9-0DB5-477E-AB75-0EDDDC680D2C",
                                "country": "IT",
                                "language": "it",
                                "order": 1,
                                "typeDescription": "Altre emissioni",
                                "subTypeDescription": "-"
                            }
                        }
                    },
                    {
                        "_id": "8C509013-17F7-44D9-8D2C-D4CD59D20963",
                        "code": "ENGINE",
                        "description": "Engine",
                        "typeCode": "ENG_BLANK",
                        "typeDescription": "",
                        "name": "Fuel injection system",
                        "unitOfMeasure": "",
                        "values": [
                            {
                                "_id": "217625B5-C1EE-49FC-9626-EBAE8FDFFDB0",
                                "value": "sfi",
                                "validFrom": "2023-03-01",
                                "validTo": "2999-12-01",
                                "final": None,
                                "languages": {},
                                "translations": {}
                            }
                        ],
                        "languages": {
                            "translations": [
                                "it-IT"
                            ],
                            "types": [
                                "it-IT"
                            ]
                        },
                        "translations": {
                            "it-IT": {
                                "_id": "C007CCEF-E1FB-4B00-A548-FF962A758F38",
                                "country": "IT",
                                "language": "it",
                                "order": 115,
                                "shortDescription": "Alimentazione",
                                "longDescription": "Alimentazione",
                                "marketingComment": None,
                                "highlight": False
                            }
                        },
                        "unitOfMeasureTranslations": {},
                        "types": {
                            "it-IT": {
                                "_id": "94E07105-4196-4D9E-85F1-BC2C93FAC7F1",
                                "country": "IT",
                                "language": "it",
                                "order": 9,
                                "typeDescription": "Motore",
                                "subTypeDescription": "-"
                            }
                        }
                    },
                    {
                        "_id": "62DDD2CE-0939-46A6-8DFB-50CB9AD8445E",
                        "code": "PERFORMANC",
                        "description": "Performance",
                        "typeCode": "PERF_BLANK",
                        "typeDescription": "",
                        "name": "0-100km/h",
                        "unitOfMeasure": "s",
                        "values": [
                            {
                                "_id": "C8F2D5A0-2E32-4D54-8D6A-EBC6011954DA",
                                "value": "7.74",
                                "validFrom": "2023-03-01",
                                "validTo": "2999-12-01",
                                "final": None,
                                "languages": {},
                                "translations": {}
                            }
                        ],
                        "languages": {
                            "translations": [
                                "it-IT"
                            ],
                            "types": [
                                "it-IT"
                            ]
                        },
                        "translations": {
                            "it-IT": {
                                "_id": "B6F75E6F-E565-4D0E-BA99-128EF7A785E9",
                                "country": "IT",
                                "language": "it",
                                "order": 140,
                                "shortDescription": "Accelerazione 0-100 km/h",
                                "longDescription": "Accelerazione 0-100 km/h",
                                "marketingComment": None,
                                "highlight": False
                            }
                        },
                        "unitOfMeasureTranslations": {},
                        "types": {
                            "it-IT": {
                                "_id": "16633327-4B6D-48C5-A789-BC9FE4556214",
                                "country": "IT",
                                "language": "it",
                                "order": 11,
                                "typeDescription": "Prestazioni",
                                "subTypeDescription": "-"
                            }
                        }
                    },
                    {
                        "_id": "73A133F0-193E-4681-851C-77ACAE87A3CE",
                        "code": "INT_DIM",
                        "description": "Interior Dimensions",
                        "typeCode": "INT_BLANK",
                        "typeDescription": "",
                        "name": "Number of seats",
                        "unitOfMeasure": "",
                        "values": [
                            {
                                "_id": "2DB767B4-E175-4A1D-9AA0-EF4EA6AD299C",
                                "value": "5",
                                "validFrom": "2023-03-01",
                                "validTo": "2999-12-01",
                                "final": None,
                                "languages": {},
                                "translations": {}
                            }
                        ],
                        "languages": {
                            "translations": [
                                "it-IT"
                            ],
                            "types": [
                                "it-IT"
                            ]
                        },
                        "translations": {
                            "it-IT": {
                                "_id": "14663FCD-3FA9-4BCD-BFD6-2EF6C18591E7",
                                "country": "IT",
                                "language": "it",
                                "order": 154,
                                "shortDescription": "Numero di posti",
                                "longDescription": "Numero di posti",
                                "marketingComment": None,
                                "highlight": False
                            }
                        },
                        "unitOfMeasureTranslations": {},
                        "types": {
                            "it-IT": {
                                "_id": "73B07E47-489B-435E-B6A1-D1D814FB2434",
                                "country": "IT",
                                "language": "it",
                                "order": 5,
                                "typeDescription": "Dimensioni interne",
                                "subTypeDescription": "-"
                            }
                        }
                    },
                    {
                        "_id": "9B7CB85E-D17D-493F-A8B2-E444CAF0E85D",
                        "code": "WEIGHT",
                        "description": "Weight",
                        "typeCode": "WEIG_MASS",
                        "typeDescription": "Gross vehicle mass",
                        "name": "Total gross vehicle mass",
                        "unitOfMeasure": "kg",
                        "values": [
                            {
                                "_id": "AB5D2828-E89A-4F9D-8624-F0103430B47E",
                                "value": "2720",
                                "validFrom": "2023-03-01",
                                "validTo": "2999-12-01",
                                "final": None,
                                "languages": {},
                                "translations": {}
                            }
                        ],
                        "languages": {
                            "types": [
                                "it-IT"
                            ]
                        },
                        "translations": {},
                        "unitOfMeasureTranslations": {},
                        "types": {
                            "it-IT": {
                                "_id": "8D8FF346-3DB1-4222-9B51-53CAF38B83D6",
                                "country": "IT",
                                "language": "it",
                                "order": 10,
                                "typeDescription": "Pesi",
                                "subTypeDescription": "-"
                            }
                        }
                    },
                    {
                        "_id": "EC1C5F0C-EF44-4307-922C-DE1DCCA6F670",
                        "code": "ENGINE",
                        "description": "Engine",
                        "typeCode": "ENG_BLANK",
                        "typeDescription": "",
                        "name": "Max RPM for max torque",
                        "unitOfMeasure": "rpm",
                        "values": [
                            {
                                "_id": "83F973A7-29D8-4629-9F41-FB853437D839",
                                "value": "5200",
                                "validFrom": "2023-03-01",
                                "validTo": "2999-12-01",
                                "final": None,
                                "languages": {},
                                "translations": {}
                            }
                        ],
                        "languages": {
                            "types": [
                                "it-IT"
                            ]
                        },
                        "translations": {},
                        "unitOfMeasureTranslations": {},
                        "types": {
                            "it-IT": {
                                "_id": "94E07105-4196-4D9E-85F1-BC2C93FAC7F1",
                                "country": "IT",
                                "language": "it",
                                "order": 9,
                                "typeDescription": "Motore",
                                "subTypeDescription": "-"
                            }
                        }
                    },
                    {
                        "_id": "95DA2481-4AC0-4429-A5D5-2005B8C97BE9",
                        "code": "INT_DIM",
                        "description": "Interior Dimensions",
                        "typeCode": "INT_BLANK",
                        "typeDescription": "",
                        "name": "Interior Height",
                        "unitOfMeasure": "mm",
                        "values": [
                            {
                                "_id": "48C36E75-75D9-4FE0-922B-FDE36685737A",
                                "value": "1299",
                                "validFrom": "2023-03-01",
                                "validTo": "2999-12-01",
                                "final": None,
                                "languages": {},
                                "translations": {}
                            }
                        ],
                        "languages": {
                            "translations": [
                                "it-IT"
                            ],
                            "types": [
                                "it-IT"
                            ]
                        },
                        "translations": {
                            "it-IT": {
                                "_id": "584B0BE3-861A-4634-AFAF-82D294D060BA",
                                "country": "IT",
                                "language": "it",
                                "order": 151,
                                "shortDescription": "Altezza effettiva",
                                "longDescription": "Altezza effettiva",
                                "marketingComment": None,
                                "highlight": False
                            }
                        },
                        "unitOfMeasureTranslations": {},
                        "types": {
                            "it-IT": {
                                "_id": "73B07E47-489B-435E-B6A1-D1D814FB2434",
                                "country": "IT",
                                "language": "it",
                                "order": 5,
                                "typeDescription": "Dimensioni interne",
                                "subTypeDescription": "-"
                            }
                        }
                    }
                ],
                "colours": [
                    {
                        "fleet": None,
                        "bestseller": None,
                        "reservable": None,
                        "validFrom": None,
                        "validTo": None,
                        "lifeFrom": None,
                        "phasedoutFrom": None,
                        "suffixAvailableFromDate": "202303",
                        "suffixAvailableToDate": "202309",
                        "colourCombinations": [
                            {
                                "_id": "00064A83-2F2A-4A73-8883-651AE5DE72B9",
                                "suffixColours": [
                                    "D05A9D86-622A-4A3D-87BC-9B5F99BEF023"
                                ],
                                "_links": {
                                    "self": {
                                        "_id": "00064A83-2F2A-4A73-8883-651AE5DE72B9",
                                        "href": "https://product-ro.toyota-europe.com/TMI/models/0274AD1E-E249-42EA-9A18-0CCE782F7956/colourCombinations/00064A83-2F2A-4A73-8883-651AE5DE72B9"
                                    }
                                },
                                "_embedded": {
                                    "exterior": {
                                        "_id": "ACE0DCB9-D6E9-4ED9-B6D5-E101788F9398",
                                        "_links": {
                                            "self": {
                                                "_id": "ACE0DCB9-D6E9-4ED9-B6D5-E101788F9398",
                                                "href": "https://product-ro.toyota-europe.com/TMI/models/0274AD1E-E249-42EA-9A18-0CCE782F7956/colours/ACE0DCB9-D6E9-4ED9-B6D5-E101788F9398"
                                            }
                                        }
                                    },
                                    "interior": {
                                        "_id": "4B602ED6-226F-4FAB-8FFE-6FF2B457D4D5",
                                        "_links": {
                                            "self": {
                                                "_id": "4B602ED6-226F-4FAB-8FFE-6FF2B457D4D5",
                                                "href": "https://product-ro.toyota-europe.com/TMI/models/0274AD1E-E249-42EA-9A18-0CCE782F7956/colours/4B602ED6-226F-4FAB-8FFE-6FF2B457D4D5"
                                            }
                                        }
                                    },
                                    "trim": {
                                        "_id": "E5453BAC-F53B-4D50-9F45-46ACB91EFC59",
                                        "_links": {
                                            "self": {
                                                "_id": "E5453BAC-F53B-4D50-9F45-46ACB91EFC59",
                                                "href": "https://product-ro.toyota-europe.com/TMI/models/0274AD1E-E249-42EA-9A18-0CCE782F7956/colours/E5453BAC-F53B-4D50-9F45-46ACB91EFC59"
                                            }
                                        }
                                    }
                                }
                            }
                        ]
                    },
                    {
                        "fleet": None,
                        "bestseller": None,
                        "reservable": None,
                        "validFrom": None,
                        "validTo": None,
                        "lifeFrom": None,
                        "phasedoutFrom": None,
                        "suffixAvailableFromDate": "202303",
                        "suffixAvailableToDate": "202309",
                        "colourCombinations": [
                            {
                                "_id": "1749151E-E02E-4FC5-BE23-84631D9D8577",
                                "suffixColours": [
                                    "1B0BD067-30B7-474E-8538-D9F174C3B558"
                                ],
                                "_links": {
                                    "self": {
                                        "_id": "1749151E-E02E-4FC5-BE23-84631D9D8577",
                                        "href": "https://product-ro.toyota-europe.com/TMI/models/0274AD1E-E249-42EA-9A18-0CCE782F7956/colourCombinations/1749151E-E02E-4FC5-BE23-84631D9D8577"
                                    }
                                },
                                "_embedded": {
                                    "exterior": {
                                        "_id": "7F962180-9FEB-41D1-81BD-1579CA23EB54",
                                        "_links": {
                                            "self": {
                                                "_id": "7F962180-9FEB-41D1-81BD-1579CA23EB54",
                                                "href": "https://product-ro.toyota-europe.com/TMI/models/0274AD1E-E249-42EA-9A18-0CCE782F7956/colours/7F962180-9FEB-41D1-81BD-1579CA23EB54"
                                            }
                                        }
                                    },
                                    "interior": {
                                        "_id": "4B602ED6-226F-4FAB-8FFE-6FF2B457D4D5",
                                        "_links": {
                                            "self": {
                                                "_id": "4B602ED6-226F-4FAB-8FFE-6FF2B457D4D5",
                                                "href": "https://product-ro.toyota-europe.com/TMI/models/0274AD1E-E249-42EA-9A18-0CCE782F7956/colours/4B602ED6-226F-4FAB-8FFE-6FF2B457D4D5"
                                            }
                                        }
                                    },
                                    "trim": {
                                        "_id": "E5453BAC-F53B-4D50-9F45-46ACB91EFC59",
                                        "_links": {
                                            "self": {
                                                "_id": "E5453BAC-F53B-4D50-9F45-46ACB91EFC59",
                                                "href": "https://product-ro.toyota-europe.com/TMI/models/0274AD1E-E249-42EA-9A18-0CCE782F7956/colours/E5453BAC-F53B-4D50-9F45-46ACB91EFC59"
                                            }
                                        }
                                    }
                                }
                            }
                        ]
                    },
                    {
                        "fleet": None,
                        "bestseller": None,
                        "reservable": None,
                        "validFrom": None,
                        "validTo": None,
                        "lifeFrom": None,
                        "phasedoutFrom": None,
                        "suffixAvailableFromDate": "202303",
                        "suffixAvailableToDate": "202309",
                        "colourCombinations": [
                            {
                                "_id": "C370E1C1-CC7A-49CA-AA8C-AE4B6375B608",
                                "suffixColours": [
                                    "54FA719C-A714-40D7-9940-E04397E9481E"
                                ],
                                "_links": {
                                    "self": {
                                        "_id": "C370E1C1-CC7A-49CA-AA8C-AE4B6375B608",
                                        "href": "https://product-ro.toyota-europe.com/TMI/models/0274AD1E-E249-42EA-9A18-0CCE782F7956/colourCombinations/C370E1C1-CC7A-49CA-AA8C-AE4B6375B608"
                                    }
                                },
                                "_embedded": {
                                    "exterior": {
                                        "_id": "D319ED8D-76C2-407D-8EBA-B8988D753C3F",
                                        "_links": {
                                            "self": {
                                                "_id": "D319ED8D-76C2-407D-8EBA-B8988D753C3F",
                                                "href": "https://product-ro.toyota-europe.com/TMI/models/0274AD1E-E249-42EA-9A18-0CCE782F7956/colours/D319ED8D-76C2-407D-8EBA-B8988D753C3F"
                                            }
                                        }
                                    },
                                    "interior": {
                                        "_id": "4B602ED6-226F-4FAB-8FFE-6FF2B457D4D5",
                                        "_links": {
                                            "self": {
                                                "_id": "4B602ED6-226F-4FAB-8FFE-6FF2B457D4D5",
                                                "href": "https://product-ro.toyota-europe.com/TMI/models/0274AD1E-E249-42EA-9A18-0CCE782F7956/colours/4B602ED6-226F-4FAB-8FFE-6FF2B457D4D5"
                                            }
                                        }
                                    },
                                    "trim": {
                                        "_id": "E5453BAC-F53B-4D50-9F45-46ACB91EFC59",
                                        "_links": {
                                            "self": {
                                                "_id": "E5453BAC-F53B-4D50-9F45-46ACB91EFC59",
                                                "href": "https://product-ro.toyota-europe.com/TMI/models/0274AD1E-E249-42EA-9A18-0CCE782F7956/colours/E5453BAC-F53B-4D50-9F45-46ACB91EFC59"
                                            }
                                        }
                                    }
                                }
                            }
                        ]
                    },
                    {
                        "fleet": None,
                        "bestseller": None,
                        "reservable": None,
                        "validFrom": None,
                        "validTo": None,
                        "lifeFrom": None,
                        "phasedoutFrom": None,
                        "suffixAvailableFromDate": "202303",
                        "suffixAvailableToDate": "202309",
                        "colourCombinations": [
                            {
                                "_id": "08024371-5D9C-4C90-8A2A-FAE84A9ACEAE",
                                "suffixColours": [
                                    "D78B1BFD-B568-4851-961B-0CCA1B984D7C"
                                ],
                                "_links": {
                                    "self": {
                                        "_id": "08024371-5D9C-4C90-8A2A-FAE84A9ACEAE",
                                        "href": "https://product-ro.toyota-europe.com/TMI/models/0274AD1E-E249-42EA-9A18-0CCE782F7956/colourCombinations/08024371-5D9C-4C90-8A2A-FAE84A9ACEAE"
                                    }
                                },
                                "_embedded": {
                                    "exterior": {
                                        "_id": "50DABC16-A812-4F9B-9BCD-5DF6E96BFA36",
                                        "_links": {
                                            "self": {
                                                "_id": "50DABC16-A812-4F9B-9BCD-5DF6E96BFA36",
                                                "href": "https://product-ro.toyota-europe.com/TMI/models/0274AD1E-E249-42EA-9A18-0CCE782F7956/colours/50DABC16-A812-4F9B-9BCD-5DF6E96BFA36"
                                            }
                                        }
                                    },
                                    "interior": {
                                        "_id": "4B602ED6-226F-4FAB-8FFE-6FF2B457D4D5",
                                        "_links": {
                                            "self": {
                                                "_id": "4B602ED6-226F-4FAB-8FFE-6FF2B457D4D5",
                                                "href": "https://product-ro.toyota-europe.com/TMI/models/0274AD1E-E249-42EA-9A18-0CCE782F7956/colours/4B602ED6-226F-4FAB-8FFE-6FF2B457D4D5"
                                            }
                                        }
                                    },
                                    "trim": {
                                        "_id": "E5453BAC-F53B-4D50-9F45-46ACB91EFC59",
                                        "_links": {
                                            "self": {
                                                "_id": "E5453BAC-F53B-4D50-9F45-46ACB91EFC59",
                                                "href": "https://product-ro.toyota-europe.com/TMI/models/0274AD1E-E249-42EA-9A18-0CCE782F7956/colours/E5453BAC-F53B-4D50-9F45-46ACB91EFC59"
                                            }
                                        }
                                    }
                                }
                            }
                        ]
                    }
                ],
                "_links": {
                    "self": {
                        "_id": "0A281777-A8E4-44AB-B0B6-8D6D4C1275AF",
                        "href": "https://product-ro.toyota-europe.com/TMI/models/0274AD1E-E249-42EA-9A18-0CCE782F7956/localConfigurations/0A281777-A8E4-44AB-B0B6-8D6D4C1275AF"
                    },
                    "model": {
                        "_id": "0274AD1E-E249-42EA-9A18-0CCE782F7956",
                        "href": "https://product-ro.toyota-europe.com/TMI/models/0274AD1E-E249-42EA-9A18-0CCE782F7956"
                    },
                    "localGrade": {
                        "_id": "4D2FE32C-D0D9-4385-895D-3C663FFAD191",
                        "href": "https://product-ro.toyota-europe.com/TMI/models/0274AD1E-E249-42EA-9A18-0CCE782F7956/localGrades/4D2FE32C-D0D9-4385-895D-3C663FFAD191"
                    },
                    "katashikis": [
                        {
                            "_id": "22BFBEA7-B203-408D-8289-CD1D2BBE111A",
                            "href": "https://product-ro.toyota-europe.com/TMI/models/0274AD1E-E249-42EA-9A18-0CCE782F7956/katashikis/22BFBEA7-B203-408D-8289-CD1D2BBE111A"
                        }
                    ],
                    "orderableSuffixes": [
                        {
                            "_id": "D2E17A18-85C9-4479-9947-134A65B4E8B1",
                            "href": "https://product-ro.toyota-europe.com/TMI/models/0274AD1E-E249-42EA-9A18-0CCE782F7956/orderableSuffixes/D2E17A18-85C9-4479-9947-134A65B4E8B1"
                        }
                    ],
                    "localPacks": [
                        {
                            "_id": "CC17286E-7A18-4CB5-9DE3-98EA769DB93D",
                            "href": "https://product-ro.toyota-europe.com/TMI/models/0274AD1E-E249-42EA-9A18-0CCE782F7956/packs/CC17286E-7A18-4CB5-9DE3-98EA769DB93D"
                        }
                    ],
                    "endUserEquipments": {
                        "href": "https://product-ro.toyota-europe.com/TMI/models/0274AD1E-E249-42EA-9A18-0CCE782F7956/endUserEquipments?localConfigurationId=0A281777-A8E4-44AB-B0B6-8D6D4C1275AF"
                    }
                },
                "_embedded": {
                    "localGrade": {
                        "_id": "4D2FE32C-D0D9-4385-895D-3C663FFAD191",
                        "description": "Lounge"
                    }
                }
            }
        ]
    }
})
print(f"Waiting for tx {txid} to be completed")
if gs.wait_for_transacioon_to_complete(txid, 120):
    print("Transaction comleted")
else:
    print("Transaction still on going after 120 seconds")
"""
txs = gs.listtransactions(None, 1, 0, False)
print (txs)

"""
Esempio per ottenere l'help:

help = api.help()
print(help)
"""

"""
Esempio per ottenere le info sulla block chain cui si è collegati:
info = api.getinfo()
print("Chain Name: %s - Versione: %s - Edition: %s" % (info['chainname'], info['version'], info['edition']))
"""
