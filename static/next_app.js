(function (nx) {
  /**
   * NeXt UI base application
   */
  // Initialize topology
  var topo = new nx.graphic.Topology({
    // View dimensions
    width: window.innerWidth,
    height: window.innerHeight,
    // Dataprocessor is responsible for spreading
    // the Nodes across the view.
    // 'force' dataprocessor spreads the Nodes so
    // they would be as distant from each other
    // as possible. Follow social distancing and stay healthy.
    // 'quick' dataprocessor picks random positions
    // for the Nodes.
    dataProcessor: "force",
    // Node and Link identity key attribute name
    identityKey: "id",
    // Node settings
    nodeConfig: {
      label: "model.name",
      iconType: "model.icon",
      color: function (model) {
        status = nodeReservationData[model._data.name]
        if (status === "None" || status === "FREE"){
          return "#077d0d";
        }
        else if (status === "ETA EXPIRED") {
          return "#b8ae07";
        }
        else if (status === "OCCUPIED") {
          return "#a12500";
        }
      },
    },
    // Node Set settings (for future use)
    nodeSetConfig: {
      label: "model.name",
      iconType: "model.iconType",
    },
    // Tooltip content settings
    tooltipManagerConfig: {
      nodeTooltipContentClass: "CustomNodeTooltip",
      linkTooltipContentClass: "MyLinkTooltip",
    },
    // Link settings
    linkConfig: {
      // Display Links as curves in case of
      //multiple links between Node Pairs.
      // Set to 'parallel' to use parallel links.
      linkType: "curve",
      sourcelabel: "model.srcIfName",
      targetlabel: "model.tgtIfName",
      style: function (model) {
        if (model._data.is_dead === "yes") {
          return { "stroke-dasharray": "5" };
        }
      },
      color: function (model) {
        if (model._data.is_dead === "yes") {
          return "#E40039";
        }
        if (model._data.is_new === "yes") {
          return "#148D09";
        }
      },
    },
    // Display Node icon. Displays a dot if set to 'false'.
    showIcon: true,
    //   linkInstanceClass: "CustomLinkClass",
  });

  topo.registerIcon("dead_node", "img/dead_node.png", 49, 49);

  var Shell = nx.define(nx.ui.Application, {
    methods: {
      start: function () {
        // Read topology data from variable
        topo.data(topologyData);
        // Attach it to the document
        topo.attach(this);
      },
    },
  });

  nx.define("MyLinkTooltip", nx.ui.Component, {
    properties: {
      node: {},
      link: {},
      topology: {},
    },
    view: {
      content: [
        {
          tag: "p",
          content: [
            {
              tag: "label",
              tag: "b",
              content: "SrcDevice: ",
            },
            {
              tag: "p",
              content: "{#link.model.srcDevice}",
            },
            {
              tag: "label",
              tag: "b",
              content: "SrcIntf: ",
            },
            {
              tag: "p",
              content: "{#link.model.srcIfName}",
            },
            {
              tag: "label",
              tag: "b",
              content: "TgtDevice: ",
            },
            {
              tag: "p",
              content: "{#link.model.tgtDevice}",
            },
            {
              tag: "label",
              tag: "b",
              content: "TgtIntf: ",
            },
            {
              tag: "p",
              content: "{#link.model.tgtIfName}",
            },
          ],
        },
      ],
    },
  });
  nx.define("Tooltip.Link", nx.ui.Component, {
    view: {
      content: {
        name: "topo",
        type: "nx.graphic.Topology",
        props: {
          adaptive: true,
          nodeConfig: {
            label: "model.id",
          },
          linkConfig: {
            linkType: "curve",
          },
          tooltipManagerConfig: {
            linkTooltipContentClass: "MyLinkTooltip",
          },
          showIcon: true,
          data: topologyData,
        },
      },
    },
    methods: {
      attach: function (args) {
        this.inherited(args);
        this.model(mainModel);
      },
    },
  });

  nx.define("CustomNodeTooltip", nx.ui.Component, {
    properties: {
      node: {},
      topology: {},
    },
    view: {
      content: [
        {
          tag: "div",
          content: [
            {
              tag: "h5",
              content: [
                {
                  tag: "a",
                  content: "{#node.model.name}",
                  props: { href: "{#node.model.dcimDeviceLink}" },
                },
              ],
              props: {
                style:
                  "border-bottom: dotted 1px; font-size:90%; word-wrap:normal; color:#003688",
              },
            },
            {
              tag: "p",
              content: [
                {
                  tag: "label",
                  content: "Telnet IP: ",
                },
                {
                  tag: "label",
                  content: "{#node.model.telnetIP}",
                },
              ],
              props: {
                style: "font-size:80%;",
              },
            },
            {
              tag: "p",
              content: [
                {
                  tag: "label",
                  content: "Telnet Port: ",
                },
                {
                  tag: "label",
                  content: "{#node.model.telnetPort}",
                },
              ],
              props: {
                style: "font-size:80%;",
              },
            },
            {
              tag: "p",
              content: [
                {
                  tag: "label",
                  content: "TGEN: ",
                },
                {
                  tag: "label",
                  content: "{#node.model.tgen}",
                },
              ],
              props: {
                style: "font-size:80%;",
              },
            },
            {
              tag: "p",
              content: [
                {
                  tag: "label",
                  content: "Project: ",
                },
                {
                  tag: "label",
                  content: "{#node.model.project}",
                },
              ],
              props: {
                style: "font-size:80%;",
              },
            },
          ],
          props: {
            style: "width: 150px;",
          },
        },
      ],
    },
  });

  nx.define("Tooltip.Node", nx.ui.Component, {
    view: function (view) {
      view.content.push({});
      return view;
    },
    methods: {
      attach: function (args) {
        this.inherited(args);
        this.model();
      },
    },
  });

  nx.define("CustomLinkClass", nx.graphic.Topology.Link, {
    properties: {
      sourcelabel: null,
      targetlabel: null,
    },
    view: function (view) {
      view.content.push(
        {
          name: "source",
          type: "nx.graphic.Text",
          props: {
            class: "sourcelabel",
            "alignment-baseline": "text-after-edge",
            "text-anchor": "start",
          },
        },
        {
          name: "target",
          type: "nx.graphic.Text",
          props: {
            class: "targetlabel",
            "alignment-baseline": "text-after-edge",
            "text-anchor": "end",
          },
        }
      );

      return view;
    },
    methods: {
      update: function () {
        this.inherited();

        var el, point;

        var line = this.line();
        var angle = line.angle();
        var stageScale = this.stageScale();

        // pad line
        line = line.pad(18 * stageScale, 18 * stageScale);

        if (this.sourcelabel()) {
          el = this.view("source");
          point = line.start;
          el.set("x", point.x);
          el.set("y", point.y);
          el.set("text", this.sourcelabel());
          el.set(
            "transform",
            "rotate(" + angle + " " + point.x + "," + point.y + ")"
          );
          el.setStyle("font-size", 12 * stageScale);
        }

        if (this.targetlabel()) {
          el = this.view("target");
          point = line.end;
          el.set("x", point.x);
          el.set("y", point.y);
          el.set("text", this.targetlabel());
          el.set(
            "transform",
            "rotate(" + angle + " " + point.x + "," + point.y + ")"
          );
          el.setStyle("font-size", 12 * stageScale);
        }
      },
    },
  });

  var currentLayout = "auto";

  horizontal = function () {
    if (currentLayout === "horizontal") {
      return;
    }
    currentLayout = "horizontal";
    var layout = topo.getLayout("hierarchicalLayout");
    layout.direction("horizontal");
    layout.levelBy(function (node, model) {
      return model.get("layerSortPreference");
    });
    topo.activateLayout("hierarchicalLayout");
  };

  vertical = function () {
    if (currentLayout === "vertical") {
      return;
    }
    currentLayout = "vertical";
    var layout = topo.getLayout("hierarchicalLayout");
    layout.direction("vertical");
    layout.levelBy(function (node, model) {
      return model.get("layerSortPreference");
    });
    topo.activateLayout("hierarchicalLayout");
  };

  update_reservations = async function() {
    topo.showLoading()
    const request = fetch("/update")
    update_btn = document.getElementById("update-btn")
    update_btn.innerHTML = "Loading..."
    request.then((response)=>{
      return response.text()
    }).then(()=>{window.location.reload()})
  }
  // Create an application instance
  var shell = new Shell();
  // Run the application
  shell.start();
})(nx);