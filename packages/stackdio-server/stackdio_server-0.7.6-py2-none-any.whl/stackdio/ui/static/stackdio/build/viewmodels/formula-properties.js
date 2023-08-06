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

define(["jquery","knockout","bootbox","models/formula"],function(r,e,o,t){"use strict";return function(){var r=this;r.breadcrumbs=[{active:!1,title:"Formulas",href:"/formulas/"},{active:!1,title:window.stackdio.formulaTitle,href:"/formulas/"+window.stackdio.formulaId+"/"},{active:!0,title:"Default Properties"}],r.validProperties=!0,r.formula=new t(window.stackdio.formulaId),r.propertiesJSON=e.pureComputed({read:function(){return e.toJSON(r.formula.properties(),null,3)},write:function(e){try{r.formula.properties(JSON.parse(e)),r.validProperties=!0}catch(o){r.validProperties=!1}}}),r.saveProperties=function(){return r.validProperties?void r.formula.saveProperties():void o.alert({title:"Error saving properties",message:"The properties field must contain valid JSON."})},r.reload=function(){r.formula.loadProperties()},r.reload()}});