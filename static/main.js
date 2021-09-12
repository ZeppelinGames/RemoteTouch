const Keyboard = SimpleKeyboard.default;

const keyboard = new Keyboard({
  onKeyPress: button => onKeyPress(button),
  onKeyReleased : button => onKeyReleased(button),
  useMouseEvents : true,
  useTouchEvents : true,
  theme: "hg-theme-default hg-layout-default keys-black",
  
  display: {
    '{bksp}': 'del',
    '{enter}': 'return',
    '{shift}': 'shift',
    '{tab}': 'tab',
    '{lock}': 'caps',
    '{space}':'____________________',
    '{ctrl}' : 'ctrl',
    '{alt}' :'alt',
    '{f1}' : 'f1',
    '{f2}' : 'f2',
    '{f3}' : 'f3',
    '{f4}' : 'f4',
    '{f5}' : 'f5',
    '{f6}' : 'f6',
    '{f7}' : 'f7',
    '{f8}' : 'f8',
    '{f9}' : 'f9',
    '{f10}' : 'f10',
    '{f11}' : 'f11',
    '{f12}' : 'f12',
    '{esc}' : 'esc'
  },

  layout: {
    'default': [
      '{esc} {f1} {f2} {f3} {f4} {f5} {f6} {f7} {f8} {f9} {f10} {f11} {f12}',
      '` 1 2 3 4 5 6 7 8 9 0 - = {bksp}',
      '{tab} q w e r t y u i o p [ ] \\',
      '{lock} a s d f g h j k l ; \' {enter}',
      '{shift} z x c v b n m , . / {shift}',
      '{ctrl} {space} {alt}'
    ],
    'shift': [
      '{esc} {f1} {f2} {f3} {f4} {f5} {f6} {f7} {f8} {f9} {f10} {f11} {f12}',
      '~ ! @ # $ % ^ & * ( ) _ + {bksp}',
      '{tab} Q W E R T Y U I O P { } |',
      '{lock} A S D F G H J K L : " {enter}',
      '{shift} Z X C V B N M < > ? {shift}',
      '{ctrl} {space} {alt}'
    ]
  },

  buttonTheme: [
    {
      class: "keys-black",
      buttons: '{tab} {lock} {shift} {ctrl} {alt} {bksp} {f5} {f6} {f7} {f8}'
    },
    {
      class: "keys-highlight",
      buttons: '{esc} {enter}'
    }
  ]
});

const lmb = document.getElementById("lmb");
const scroll = document.getElementById("scoll");
const rmb  = document.getElementById("rmb");

lmb.ontouchstart = function() { lmbDown(); }
lmb.ontouchend = function() { lmbUP(); }

rmb.ontouchstart = function() { rmbDown(); }
rmb.ontouchend = function() { rmbUp(); }

const trackpadDiv = document.getElementById("Trackpad");
// trackpadDiv.addEventListener('onmousemove', (event) => {
//   mouseMoved(event.clientX, event.clientY);
// });
//onmousemove = onmousedown = function(event) { mouseMoved(event.clientX,event.clientY);}
trackpadDiv.ontouchmove = function(event) {mouseMoved(event.touches[0].clientX, event.touches[0].clientY);}

var upperActive = false;
var upperLocked = false;

function onKeyPress(button) {
  console.log("Button pressed", button);
  postData(["kd",button]);

  if (button == "{shift}") {
    handleShift();
  }
  if (button == "{lock}") {
    upperLocked = !upperLocked;
    handleShift();
  }
}

function onKeyReleased(button) {
  console.log("Button released", button);
  postData(["ku",button]);

  if (button == "{shift}") {
    handleShift();
  }
}

function mouseMoved(x, y) {
  console.log(x,", ", y);
  postData(["mm", x, y]);
}

function lmbDown() {
  console.log("LMB down");
  postData(["lmbd"]);
}

function lmbUp() {
  console.log("LMB up");
  postData(["lmbu"]);
}

function rmbDown() {
  console.log("RMB down");
  postData(["rmbd"]);
}

function rmbUp() {
  console.log("RMB up");
  postData(["rmbu"]);
}

function handleShift() {
  if(!upperLocked) upperActive = !upperActive;

  keyboard.setOptions({
    layoutName: (upperActive ? "shift" : "default") 
  });
}

function postData(data) {
  var xmlHttp = new XMLHttpRequest();
  xmlHttp.open('POST','/',true);
  xmlHttp.setRequestHeader('Content-type', 'application/x-www-form-urlencoded')

  let postDataStr = "inputData="
  for(let i=0; i < data.length-1; i++) {
    postDataStr += data[i] + ":";
  }
  postDataStr += data[data.length-1];

  xmlHttp.send(postDataStr);
}