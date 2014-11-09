/*global famous*/
// import dependencies
var Engine = famous.core.Engine;
var Surface = famous.core.Surface;

var mainContext = Engine.createContext();

var firstSurface = new Surface({
    content: "<h3>Hi!</h3>",
    size: [200, 200],
    properties: {
        backgroundColor: 'rgb(240, 238, 233)',
        textAlign: 'center',
        padding: '5px',
        border: '2px solid rgb(210, 208, 203)',
        marginTop: '50px',
        marginLeft: '50px'
    }
});


mainContext.add(firstSurface);
