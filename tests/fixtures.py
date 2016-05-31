example_get_car = {
    'data': {
        'type': 'Car',
        'id': '1',
        'attributes': {
            'name': 'Ka',
            'created_at': '2016-05-20T10:50:23.037000Z',
            'updated_at': '2016-05-20T10:50:23.037000Z'
        },
        'relationships': {
            'manufacturer': {
                'data': {
                    'type': 'Manufacturer',
                    'id': '1'
                },
                'links': {
                    'related': 'http://localhost:8000/api/v1/manufacturers/1/'
                }
            }
        },
        'links': {
            'self': 'http://localhost:8000/api/v1/cars/1/'
        }
    }
}

example_get_cars = {
    'links': {
        'first': 'http://localhost:8000/api/v1/cars/?page=1',
        'last': 'http://localhost:8000/api/v1/cars/?page=2',
        'next': 'http://localhost:8000/api/v1/cars/?page=2',
        'prev': None
    },
    'data': [
        {
            'type': 'Car',
            'id': '1',
            'attributes': {
                'name': 'Ka',
                'created_at': '2016-05-20T10:50:23.037000Z',
                'updated_at': '2016-05-20T10:50:23.037000Z'
            },
            'relationships': {
                'manufacturer': {
                    'data': {
                        'type': 'Manufacturer',
                        'id': '1'
                    },
                    'links': {
                        'related': 'http://localhost:8000/api/v1/manufacturers/1/'
                    }
                }
            },
            'links': {
                'self': 'http://localhost:8000/api/v1/cars/1/'
            }
        },
        {
            'type': 'Car',
            'id': '2',
            'attributes': {
                'name': 'Fiesta',
                'created_at': '2016-05-20T10:50:29.988000Z',
                'updated_at': '2016-05-20T10:50:29.988000Z'
            },
            'relationships': {
                'manufacturer': {
                    'data': {
                        'type': 'Manufacturer',
                        'id': '1'
                    },
                    'links': {
                        'related': 'http://localhost:8000/api/v1/manufacturers/1/'
                    }
                }
            },
            'links': {
                'self': 'http://localhost:8000/api/v1/cars/2/'
            }
        },
        {
            'type': 'Car',
            'id': '3',
            'attributes': {
                'name': 'B-MAX',
                'created_at': '2016-05-20T10:50:38.338000Z',
                'updated_at': '2016-05-20T10:50:38.338000Z'
            },
            'relationships': {
                'manufacturer': {
                    'data': {
                        'type': 'Manufacturer',
                        'id': '1'
                    },
                    'links': {
                        'related': 'http://localhost:8000/api/v1/manufacturers/1/'
                    }
                }
            },
            'links': {
                'self': 'http://localhost:8000/api/v1/cars/3/'
            }
        },
        {
            'type': 'Car',
            'id': '4',
            'attributes': {
                'name': 'Ford EcoSport',
                'created_at': '2016-05-20T10:50:49.900000Z',
                'updated_at': '2016-05-20T10:50:49.900000Z'
            },
            'relationships': {
                'manufacturer': {
                    'data': {
                        'type': 'Manufacturer',
                        'id': '1'
                    },
                    'links': {
                        'related': 'http://localhost:8000/api/v1/manufacturers/1/'
                    }
                }
            },
            'links': {
                'self': 'http://localhost:8000/api/v1/cars/4/'
            }
        },
        {
            'type': 'Car',
            'id': '5',
            'attributes': {
                'name': 'Focus',
                'created_at': '2016-05-20T10:50:57.731000Z',
                'updated_at': '2016-05-20T10:50:57.731000Z'
            },
            'relationships': {
                'manufacturer': {
                    'data': {
                        'type': 'Manufacturer',
                        'id': '1'
                    },
                    'links': {
                        'related': 'http://localhost:8000/api/v1/manufacturers/1/'
                    }
                }
            },
            'links': {
                'self': 'http://localhost:8000/api/v1/cars/5/'
            }
        },
        {
            'type': 'Car',
            'id': '6',
            'attributes': {
                'name': 'C-MAX',
                'created_at': '2016-05-20T10:51:03.852000Z',
                'updated_at': '2016-05-20T10:51:03.852000Z'
            },
            'relationships': {
                'manufacturer': {
                    'data': {
                        'type': 'Manufacturer',
                        'id': '1'
                    },
                    'links': {
                        'related': 'http://localhost:8000/api/v1/manufacturers/1/'
                    }
                }
            },
            'links': {
                'self': 'http://localhost:8000/api/v1/cars/6/'
            }
        },
        {
            'type': 'Car',
            'id': '7',
            'attributes': {
                'name': 'Kuga',
                'created_at': '2016-05-20T10:51:09.319000Z',
                'updated_at': '2016-05-20T10:51:09.319000Z'
            },
            'relationships': {
                'manufacturer': {
                    'data': {
                        'type': 'Manufacturer',
                        'id': '1'
                    },
                    'links': {
                        'related': 'http://localhost:8000/api/v1/manufacturers/1/'
                    }
                }
            },
            'links': {
                'self': 'http://localhost:8000/api/v1/cars/7/'
            }
        },
        {
            'type': 'Car',
            'id': '8',
            'attributes': {
                'name': 'Mondeo',
                'created_at': '2016-05-20T10:51:15.586000Z',
                'updated_at': '2016-05-20T10:51:15.586000Z'
            },
            'relationships': {
                'manufacturer': {
                    'data': {
                        'type': 'Manufacturer',
                        'id': '1'
                    },
                    'links': {
                        'related': 'http://localhost:8000/api/v1/manufacturers/1/'
                    }
                }
            },
            'links': {
                'self': 'http://localhost:8000/api/v1/cars/8/'
            }
        },
        {
            'type': 'Car',
            'id': '9',
            'attributes': {
                'name': 'Vignale',
                'created_at': '2016-05-20T10:51:23.374000Z',
                'updated_at': '2016-05-20T10:51:23.374000Z'
            },
            'relationships': {
                'manufacturer': {
                    'data': {
                        'type': 'Manufacturer',
                        'id': '1'
                    },
                    'links': {
                        'related': 'http://localhost:8000/api/v1/manufacturers/1/'
                    }
                }
            },
            'links': {
                'self': 'http://localhost:8000/api/v1/cars/9/'
            }
        },
        {
            'type': 'Car',
            'id': '10',
            'attributes': {
                'name': 'Mustang',
                'created_at': '2016-05-20T10:51:28.998000Z',
                'updated_at': '2016-05-20T10:51:28.998000Z'
            },
            'relationships': {
                'manufacturer': {
                    'data': {
                        'type': 'Manufacturer',
                        'id': '1'
                    },
                    'links': {
                        'related': 'http://localhost:8000/api/v1/manufacturers/1/'
                    }
                }
            },
            'links': {
                'self': 'http://localhost:8000/api/v1/cars/10/'
            }
        }
    ],
    'meta': {
        'pagination': {
            'page': 1,
            'pages': 2,
            'count': 19
        }
    }
}
