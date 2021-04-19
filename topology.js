

var topologyData = {
    "links": [
        {
            "id": 0,
            "source": 0,
            "srcDevice": "Turin_2004",
            "srcIfName": "TenGigE0/0/0/0",
            "target": 1,
            "tgtDevice": "PE1",
            "tgtIfName": "TenGigE0/7/0/7"
        },
        {
            "id": 1,
            "source": 0,
            "srcDevice": "Turin_2004",
            "srcIfName": "TenGigE0/0/0/10",
            "target": 2,
            "tgtDevice": "Tortin_2019",
            "tgtIfName": "TenGigE0/0/0/10"
        },
        {
            "id": 2,
            "source": 0,
            "srcDevice": "Turin_2004",
            "srcIfName": "TenGigE0/0/0/15",
            "target": 3,
            "tgtDevice": "Bigbend_2020",
            "tgtIfName": "TenGigE0/0/0/15"
        },
        {
            "id": 3,
            "source": 4,
            "srcDevice": "Tortin_2011",
            "srcIfName": "TenGigE0/0/0/8",
            "target": 5,
            "tgtDevice": "Tortin_2008",
            "tgtIfName": "TenGigE0/0/0/8"
        },
        {
            "id": 4,
            "source": 4,
            "srcDevice": "Tortin_2011",
            "srcIfName": "TenGigE0/0/0/9",
            "target": 5,
            "tgtDevice": "Tortin_2008",
            "tgtIfName": "TenGigE0/0/0/9"
        },
        {
            "id": 5,
            "source": 4,
            "srcDevice": "Tortin_2011",
            "srcIfName": "TenGigE0/0/0/20",
            "target": 6,
            "tgtDevice": "Tortin_2005",
            "tgtIfName": "TenGigE0/0/0/20"
        },
        {
            "id": 6,
            "source": 4,
            "srcDevice": "Tortin_2011",
            "srcIfName": "HundredGigE0/0/1/1",
            "target": 7,
            "tgtDevice": "Pyke_2006",
            "tgtIfName": "HundredGigE0/0/0/1"
        },
        {
            "id": 7,
            "source": 5,
            "srcDevice": "Tortin_2008",
            "srcIfName": "TenGigE0/0/0/10",
            "target": 8,
            "tgtDevice": "Turin_2014",
            "tgtIfName": "TenGigE0/0/0/6"
        },
        {
            "id": 8,
            "source": 5,
            "srcDevice": "Tortin_2008",
            "srcIfName": "TenGigE0/0/0/11",
            "target": 8,
            "tgtDevice": "Turin_2014",
            "tgtIfName": "TenGigE0/0/0/7"
        },
        {
            "id": 9,
            "source": 5,
            "srcDevice": "Tortin_2008",
            "srcIfName": "TenGigE0/0/0/23",
            "target": 8,
            "tgtDevice": "Turin_2014",
            "tgtIfName": "TenGigE0/0/0/23"
        },
        {
            "id": 10,
            "source": 5,
            "srcDevice": "Tortin_2008",
            "srcIfName": "HundredGigE0/0/1/0",
            "target": 7,
            "tgtDevice": "Pyke_2006",
            "tgtIfName": "HundredGigE0/0/0/0"
        },
        {
            "id": 11,
            "source": 8,
            "srcDevice": "Turin_2014",
            "srcIfName": "TenGigE0/0/0/4",
            "target": 9,
            "tgtDevice": "Taihu_2027",
            "tgtIfName": "TenGigE0/0/0/4"
        },
        {
            "id": 12,
            "source": 8,
            "srcDevice": "Turin_2014",
            "srcIfName": "TenGigE0/0/0/5",
            "target": 10,
            "tgtDevice": "Tortin_2012",
            "tgtIfName": "TenGigE0/0/0/5"
        },
        {
            "id": 13,
            "source": 6,
            "srcDevice": "Tortin_2005",
            "srcIfName": "TenGigE0/0/0/6",
            "target": 11,
            "tgtDevice": "Bigbend_2017",
            "tgtIfName": "TenGigE0/0/0/4"
        },
        {
            "id": 14,
            "source": 6,
            "srcDevice": "Tortin_2005",
            "srcIfName": "TenGigE0/0/0/10",
            "target": 11,
            "tgtDevice": "Bigbend_2017",
            "tgtIfName": "TenGigE0/0/0/22"
        },
        {
            "id": 15,
            "source": 6,
            "srcDevice": "Tortin_2005",
            "srcIfName": "TenGigE0/0/0/13",
            "target": 11,
            "tgtDevice": "Bigbend_2017",
            "tgtIfName": "TenGigE0/0/0/13"
        }
    ],
    "nodes": [
        {
            "icon": "router",
            "id": 0,
            "name": "Turin_2004",
            "telnetIP": "10.64.103.82",
            "telnetPort": 2004,
            "tgen": "Ixia 10, 11"
        },
        {
            "icon": "router",
            "id": 1,
            "name": "PE1",
            "telnetIP": null,
            "telnetPort": null,
            "tgen": null
        },
        {
            "icon": "router",
            "id": 2,
            "name": "Tortin_2019",
            "telnetIP": "10.64.103.82",
            "telnetPort": 2019,
            "tgen": "Te0/0/1/0/1<->sp 1/3"
        },
        {
            "icon": "router",
            "id": 3,
            "name": "Bigbend_2020",
            "telnetIP": "10.64.103.82",
            "telnetPort": 2020,
            "tgen": "None"
        },
        {
            "icon": "router",
            "id": 4,
            "name": "Tortin_2011",
            "telnetIP": "10.64.103.82",
            "telnetPort": 2011,
            "tgen": "None"
        },
        {
            "icon": "router",
            "id": 5,
            "name": "Tortin_2008",
            "telnetIP": "10.64.103.82",
            "telnetPort": 2008,
            "tgen": "Port 9"
        },
        {
            "icon": "router",
            "id": 6,
            "name": "Tortin_2005",
            "telnetIP": "10.64.103.82",
            "telnetPort": 2005,
            "tgen": "Port 17,18"
        },
        {
            "icon": "router",
            "id": 7,
            "name": "Pyke_2006",
            "telnetIP": "10.64.103.82",
            "telnetPort": 2006,
            "tgen": "None"
        },
        {
            "icon": "router",
            "id": 8,
            "name": "Turin_2014",
            "telnetIP": "10.64.103.82",
            "telnetPort": 2014,
            "tgen": "Port 13,14"
        },
        {
            "icon": "router",
            "id": 9,
            "name": "Taihu_2027",
            "telnetIP": null,
            "telnetPort": null,
            "tgen": null
        },
        {
            "icon": "router",
            "id": 10,
            "name": "Tortin_2012",
            "telnetIP": "10.64.103.82",
            "telnetPort": 2012,
            "tgen": "Port 16,28"
        },
        {
            "icon": "router",
            "id": 11,
            "name": "Bigbend_2017",
            "telnetIP": "10.64.103.82",
            "telnetPort": 2017,
            "tgen": "None"
        }
    ]
};