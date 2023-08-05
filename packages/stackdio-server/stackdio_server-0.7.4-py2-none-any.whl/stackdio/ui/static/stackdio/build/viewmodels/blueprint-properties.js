/*!
  * Copyright 2014,  Digital Reasoning
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

define(["jquery","knockout","bootbox","models/blueprint"],function(e,t,n,r){"use strict";return function(){var e=this;e.blueprint=new r(window.stackdio.blueprintId),e.breadcrumbs=[{active:!1,title:"Blueprints",href:"/blueprints/"},{active:!1,title:window.stackdio.blueprintTitle,href:"/blueprints/"+window.stackdio.blueprintId+"/"},{active:!0,title:"Properties"}],e.validProperties=!0,e.propertiesJSON=t.pureComputed({read:function(){return t.toJSON(e.blueprint.properties(),null,3)},write:function(t){try{e.blueprint.properties(JSON.parse(t)),e.validProperties=!0}catch(n){e.validProperties=!1}}}),e.saveProperties=function(){if(!e.validProperties){n.alert({title:"Error saving properties",message:"The properties field must contain valid JSON."});return}e.blueprint.saveProperties()},e.reload=function(){e.blueprint.loadProperties()},e.reload()}});