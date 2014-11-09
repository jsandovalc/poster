/*global famous*/
// import dependencies
var Engine = famous.core.Engine;
var TextAreaSurface = famous.surfaces.TextareaSurface;
var Surface = famous.core.Surface;
var Transform = famous.core.Transform;
var StateModifier = famous.modifiers.StateModifier;

var mainContext = Engine.createContext();

var textAreaSurface = new TextAreaSurface({
    size: [200, 100]
});

textAreaSurface.setPlaceholder('Post it!');

var centerModifier = new StateModifier({
    align: [0.5, 0.5],
    origin: [0.5, 0.5]
});


mainContext.add(centerModifier).add(textAreaSurface);
