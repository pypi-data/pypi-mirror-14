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

define(["jquery","knockout","bootbox","models/blueprint"],function(e,r,t,i){"use strict";return function(){var e=this;e.blueprint=new i(window.stackdio.blueprintId),e.breadcrumbs=[{active:!1,title:"Blueprints",href:"/blueprints/"},{active:!1,title:window.stackdio.blueprintTitle,href:"/blueprints/"+window.stackdio.blueprintId+"/"},{active:!0,title:"Properties"}],e.validProperties=!0,e.propertiesJSON=r.pureComputed({read:function(){return r.toJSON(e.blueprint.properties(),null,3)},write:function(r){try{e.blueprint.properties(JSON.parse(r)),e.validProperties=!0}catch(t){e.validProperties=!1}}}),e.saveProperties=function(){return e.validProperties?void e.blueprint.saveProperties():void t.alert({title:"Error saving properties",message:"The properties field must contain valid JSON."})},e.reload=function(){e.blueprint.loadProperties()},e.reload()}});