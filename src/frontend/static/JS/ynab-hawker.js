"use strict";var HIDE_ANIMATION_DURATION=500;var CLOSE_BUTTON_CLASS='ym-closeButton';var CLOSE_BUTTON_SELECTOR='.'+CLOSE_BUTTON_CLASS;initialize();var initRetryCounter=0;function initialize(){if(initRetryCounter>20){return;}
initRetryCounter+=1;if(window.mParticle){window.mParticle.ready(subscribeToBrazeMessages);}
else{setTimeout(initialize,500);}}
var subscribeRetryCounter=0;function subscribeToBrazeMessages(){var _a;if(subscribeRetryCounter>20){return;}
subscribeRetryCounter+=1;if(isBrazeReady()){if((_a=window.appboy)===null||_a===void 0?void 0:_a.subscribeToNewInAppMessages){window.appboy.subscribeToNewInAppMessages(showBrazeIAM);setTimeout(function(){window.hawkerInitialized=true;window['onHawkerInitialized']&&window['onHawkerInitialized']();},500);}}
else{setTimeout(subscribeToBrazeMessages,500);}}
function isBrazeReady(){try{return window.appboy&&window.appboy.getUser();}
catch(error){var message=error.message;if(/Appboy must be initialized/.test(message)){return false;}
throw error;}}
function showBrazeIAM(inAppMessages){var message=Array.isArray(inAppMessages)?inAppMessages[0]:inAppMessages;if(!(message instanceof window.appboy.ab.InAppMessage)){window.appboy.display.showInAppMessage(message);return;}
message.animateIn=false;message.animateOut=false;var rootElement=findOrCreateRootElement();window.appboy.display.showInAppMessage(message,rootElement,function(){bindCloseButtons(rootElement,message);bindUpdateMaxHeight(rootElement);setTimeout(function(){rootElement.className=rootElement.className.replace('mod-hide','mod-show');});});}
function findOrCreateRootElement(){var element=document.querySelector('.braze-msg-root');if(element){return element;}
element=document.createElement('div');element.className='braze-msg-root mod-hide';document.body.appendChild(element);return element;}
function bindCloseButtons(rootElement,message){var _a;var frameWindow=(_a=rootElement.querySelector('iframe'))===null||_a===void 0?void 0:_a.contentWindow;if(frameWindow){var frameDocument=frameWindow.document;frameDocument.addEventListener('click',function(event){if(event.target&&isCloseButton(event.target)){closeMessage(event,rootElement,frameWindow,message);}},{capture:true,});}}
function bindUpdateMaxHeight(rootElement){var _a,_b;var frameDocument=(_b=(_a=rootElement.querySelector('iframe'))===null||_a===void 0?void 0:_a.contentWindow)===null||_b===void 0?void 0:_b.document;if(frameDocument){var messageImages=frameDocument.images;var updateRootMaxHeight=function(){return setRootMaxHeight(rootElement,frameDocument);};updateRootMaxHeight();for(var i=0;i<messageImages.length;i++){var image=messageImages[i];if(!image.complete){image.addEventListener('load',updateRootMaxHeight);}}}}
function setRootMaxHeight(rootElement,frameDocument){var messageElement=frameDocument.querySelector('.ym');if(messageElement){rootElement.style.maxHeight='';var messageHeight=messageElement.clientHeight;if(messageHeight>200&&messageHeight<=630){rootElement.style.maxHeight=messageHeight+'px';}
else{rootElement.style.maxHeight='';}}}
function isCloseButton(element){if(!element||!element.classList){return false;}
if(element.classList.contains(CLOSE_BUTTON_CLASS)){return true;}
if(element.closest){return element.closest(CLOSE_BUTTON_SELECTOR);}
if(element.parentElement){return isCloseButton(element.parentElement);}
return false;}
function closeMessage(event,rootElement,messageWindow,message){var _a,_b;if((_b=(_a=messageWindow)===null||_a===void 0?void 0:_a.appboyBridge)===null||_b===void 0?void 0:_b.closeMessage){event.preventDefault&&event.preventDefault();event.stopPropagation&&event.stopPropagation();message.subscribeToDismissedEvent(function(){return rootElement.remove();});rootElement.className=rootElement.className.replace('mod-show','mod-hide');setTimeout(function(){var _a,_b;if((_b=(_a=messageWindow)===null||_a===void 0?void 0:_a.appboyBridge)===null||_b===void 0?void 0:_b.closeMessage){messageWindow.appboyBridge.closeMessage();}},HIDE_ANIMATION_DURATION);}}