/*!
  * Copyright 2016,  Digital Reasoning
  * 
  * Licensed under the Apache License, Version 2.0 (the "License");
  * you may not use this file except in compliance with the License.
  * You may obtain a copy of the License at
  * 
  *     http://www.apache.org/licenses/LICENSE-2.0
  * 
  * Unless required by applicable law or agreed to in writing, software
  * distributed under the License is distributed on an "AS IS" BASIS,
  * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  * See the License for the specific language governing permissions and
  * limitations under the License.
  * 
*/

define(["jquery","knockout","bootbox","models/stack"],function(t,e,r,i){"use strict";return function(){var t=this;t.breadcrumbs=[{active:!1,title:"Stacks",href:"/stacks/"},{active:!1,title:window.stackdio.stackTitle,href:"/stacks/"+window.stackdio.stackId+"/"},{active:!0,title:"Properties"}],t.validProperties=!0,t.stack=new i(window.stackdio.stackId),t.propertiesJSON=e.pureComputed({read:function(){return e.toJSON(t.stack.properties(),null,3)},write:function(e){try{t.stack.properties(JSON.parse(e)),t.validProperties=!0}catch(r){t.validProperties=!1}}}),t.saveProperties=function(){return t.validProperties?void t.stack.saveProperties():void r.alert({title:"Error saving properties",message:"The properties field must contain valid JSON."})},t.reload=function(){t.stack.loadProperties()},t.reload()}});