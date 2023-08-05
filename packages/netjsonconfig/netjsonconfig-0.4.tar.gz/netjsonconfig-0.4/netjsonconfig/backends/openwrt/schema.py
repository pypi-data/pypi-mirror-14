"""
OpenWrt specific JSON-Schema definition
"""
from ...schema import schema as default_schema
from ...utils import merge_config
from .timezones import timezones

DEFAULT_FILE_MODE = '0644'

schema = merge_config(default_schema, {
    "definitions": {
        "other_address": {
            "type": "object",
            "title": "other",
            "allOf": [
                {"$ref": "#/definitions/base_address"},
                {
                    "type": "object",
                    "properties": {
                        "family": {"enum": ["ipv4", "ipv6"]},
                        "proto": {
                            "enum": [
                                'ppp',
                                'pppoe',
                                'pppoa',
                                '3g',
                                'qmi',
                                'ncm',
                                'hnet',
                                'pptp',
                                '6in4',
                                'aiccu',
                                '6to4',
                                '6rd',
                                'dslite',
                                'l2tp',
                                'relay',
                                'gre',
                                'gretap',
                                'grev6',
                                'grev6tap',
                                'none'
                            ]
                        }
                    }
                }
            ]
        },
        "interface_settings": {
            "properties": {
                "network": {
                    "type": "string",
                    "maxLength": 15,
                    "pattern": "^[a-zA-z0-9_\\.\\-]*$",
                    "propertyOrder": 7
                },
                "addresses": {
                    "items": {
                        "oneOf": [{"$ref": "#/definitions/other_address"}]
                    }
                }
            }
        },
        "wireless_interface": {
            "properties": {
                "wireless": {
                    "properties": {
                        "network": {
                            "type": "array",
                            "title": "Attached Networks",
                            "uniqueItems": True,
                            "additionalItems": True,
                            "items": {
                                "title": "network",
                                "type": "string",
                                "$ref": "#/definitions/interface_settings/properties/network"
                            },
                            "propertyOrder": 19
                        }
                    }
                }
            }
        },
        "wmm_wireless_property": {
            "properties": {
                "wmm": {
                    "type": "boolean",
                    "title": "WMM (802.11e)",
                    "default": True,
                    "format": "checkbox",
                    "propertyOrder": 8,
                }
            }
        },
        "macfilter_wireless": {
            "properties": {
                "macfilter": {
                    "type": "string",
                    "title": "MAC Filter",
                    "enum": [
                        "disable",
                        "allow",
                        "deny",
                    ],
                    "default": "disable",
                    "propertyOrder": 15,
                },
                "maclist": {
                    "type": "array",
                    "title": "MAC List",
                    "propertyOrder": 16,
                    "items": {
                        "type": "string",
                        "title": "MAC address",
                        "maxLength": 17,
                        "minLength": 17,
                    }
                }
            }
        },
        "ap_wireless_settings": {
            "allOf": [
                {"$ref": "#/definitions/wmm_wireless_property"},
                {"$ref": "#/definitions/macfilter_wireless"},
            ]
        },
    },
    "properties": {
        "general": {
            "properties": {
                "timezone": {
                    "type": "string",
                    "default": "UTC",
                    "enum": list(timezones.keys()),
                    "propertyOrder": 1,
                }
            }
        },
        "radios": {
            "items": {
                "required": [
                    "driver",
                    "protocol"
                ],
                "properties": {
                    "driver": {
                        "type": "string",
                        "enum": [
                            "mac80211",
                            "madwifi",
                            "ath5k",
                            "ath9k",
                            "broadcom"
                        ],
                        "propertyOrder": 0,
                    },
                    "protocol": {
                        "type": "string",
                        "enum": [
                            "802.11a",
                            "802.11b",
                            "802.11g",
                            "802.11n",
                            "802.11ac"
                        ],
                        "propertyOrder": 1,
                    }
                }
            }
        },
        "routes": {
            "items": {
                "properties": {
                    "type": {
                        "type": "string",
                        "enum": [
                            "unicast",
                            "local",
                            "broadcast",
                            "multicast",
                            "unreachable",
                            "prohibit",
                            "blackhole",
                            "anycast"
                        ],
                        "default": "unicast",
                        "propertyOrder": 0,
                    },
                    "mtu": {
                        "type": "string",
                        "title": "MTU",
                        "propertyOrder": 6,
                        "pattern": "^[0-9]*$",
                    },
                    "table": {
                        "type": "string",
                        "propertyOrder": 7,
                        "pattern": "^[0-9]*$",
                    },
                    "onlink": {
                        "type": "boolean",
                        "default": False,
                        "format": "checkbox",
                        "propertyOrder": 8,
                    }
                }
            }
        },
        "ip_rules": {
            "type": "array",
            "title": "Policy routing",
            "uniqueItems": True,
            "additionalItems": True,
            "propertyOrder": 7,
            "items": {
                "type": "object",
                "title": "IP rule",
                "additionalProperties": True,
                "properties": {
                    "in": {
                        "type": "string",
                        "propertyOrder": 1,
                    },
                    "out": {
                        "type": "string",
                        "propertyOrder": 2,
                    },
                    "src": {
                        "type": "string",
                        "propertyOrder": 3,
                    },
                    "dest": {
                        "type": "string",
                        "propertyOrder": 4,
                    },
                    "tos": {
                        "type": "integer",
                        "propertyOrder": 5,
                    },
                    "mark": {
                        "type": "string",
                        "propertyOrder": 6,
                    },
                    "lookup": {
                        "type": "string",
                        "propertyOrder": 7,
                    },
                    "action": {
                        "type": "string",
                        "enum": [
                            "prohibit",
                            "unreachable",
                            "blackhole",
                            "throw"
                        ],
                        "propertyOrder": 8,
                    },
                    "goto": {
                        "type": "integer",
                        "propertyOrder": 9,
                    },
                    "invert": {
                        "type": "boolean",
                        "default": False,
                        "format": "checkbox",
                        "propertyOrder": 10,
                    }
                }
            }
        },
        "ntp": {
            "type": "object",
            "title": "NTP Settings",
            "additionalProperties": True,
            "propertyOrder": 8,
            "properties": {
                "enabled": {
                    "type": "boolean",
                    "default": True,
                    "format": "checkbox",
                    "propertyOrder": 1,
                },
                "enable_server": {
                    "type": "boolean",
                    "title": "enable server",
                    "default": False,
                    "format": "checkbox",
                    "propertyOrder": 2,
                },
                "server": {
                    "title": "NTP Servers",
                    "type": "array",
                    "uniqueItems": True,
                    "additionalItems": True,
                    "propertyOrder": 3,
                    "items": {
                        "title": "NTP server",
                        "type": "string"
                    },
                    "default": [
                        "0.openwrt.pool.ntp.org",
                        "1.openwrt.pool.ntp.org",
                        "2.openwrt.pool.ntp.org",
                        "3.openwrt.pool.ntp.org",
                    ]
                }
            }
        },
        "switch": {
            "type": "array",
            "uniqueItems": True,
            "additionalItems": True,
            "title": "Programmable Switch",
            "propertyOrder": 9,
            "items": {
                "title": "Switch",
                "type": "object",
                "additionalProperties": True,
                "required": [
                    "name",
                    "reset",
                    "enable_vlan",
                    "vlan"
                ],
                "properties": {
                    "name": {
                        "type": "string",
                        "propertyOrder": 1,
                    },
                    "reset": {
                        "type": "boolean",
                        "default": True,
                        "format": "checkbox",
                        "propertyOrder": 2,
                    },
                    "enable_vlan": {
                        "type": "boolean",
                        "title": "enable vlan",
                        "default": True,
                        "format": "checkbox",
                        "propertyOrder": 3,
                    },
                    "vlan": {
                        "type": "array",
                        "title": "VLANs",
                        "uniqueItems": True,
                        "additionalItems": True,
                        "propertyOrder": 4,
                        "items": {
                            "type": "object",
                            "title": "VLAN",
                            "additionalProperties": True,
                            "required": [
                                "device",
                                "vlan",
                                "ports"
                            ],
                            "properties": {
                                "device": {
                                    "type": "string",
                                    "propertyOrder": 1,
                                },
                                "vlan": {
                                    "type": "integer",
                                    "propertyOrder": 2,
                                },
                                "ports": {
                                    "type": "string",
                                    "propertyOrder": 3,
                                }
                            }
                        }
                    }
                }
            }
        },
        "led": {
            "type": "array",
            "title": "LEDs",
            "uniqueItems": True,
            "additionalItems": True,
            "propertyOrder": 10,
            "items": {
                "type": "object",
                "title": "LED",
                "additionalProperties": True,
                "required": [
                    "name",
                    "sysfs",
                    "trigger"
                ],
                "properties": {
                    "name": {
                        "type": "string",
                        "propertyOrder": 1,
                    },
                    "default": {
                        "type": "boolean",
                        "format": "checkbox",
                        "propertyOrder": 2,
                    },
                    "dev": {
                        "type": "string",
                        "propertyOrder": 3,
                    },
                    "sysfs": {
                        "type": "string",
                        "propertyOrder": 4,
                    },
                    "trigger": {
                        "type": "string",
                        "propertyOrder": 5,
                    },
                    "delayoff": {
                        "type": "integer",
                        "propertyOrder": 6,
                    },
                    "delayon": {
                        "type": "integer",
                        "propertyOrder": 7,
                    },
                    "interval": {
                        "type": "integer",
                        "propertyOrder": 8,
                    },
                    "message": {
                        "type": "string",
                        "propertyOrder": 9,
                    },
                    "mode": {
                        "type": "string",
                        "propertyOrder": 10,
                    }
                }
            }
        },
        "files": {
            "type": "array",
            "title": "Files",
            "uniqueItems": True,
            "additionalItems": True,
            "propertyOrder": 11,
            "items": {
                "type": "object",
                "title": "File",
                "additionalProperties": False,
                "required": [
                    "path",
                    "mode",
                    "contents"
                ],
                "properties": {
                    "path": {
                        "type": "string",
                        "propertyOrder": 1,
                    },
                    "mode": {
                        "type": "string",
                        "maxLength": 4,
                        "minLength": 3,
                        "pattern": "^[0-7]*$",
                        "default": DEFAULT_FILE_MODE,
                        "propertyOrder": 2,
                    },
                    "contents": {
                        "type": "string",
                        "format": "textarea",
                        "propertyOrder": 3,
                    },
                }
            }
        }
    }
})
