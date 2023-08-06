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

define(["jquery","knockout","models/blueprint"],function(i,t,e){"use strict";return function(){var n=this;n.blueprint=null,n.blueprintUrl=t.observable(""),n.breadcrumbs=[{active:!1,title:"Blueprints",href:"/blueprints/"},{active:!0,title:window.stackdio.blueprintTitle}],n.subscription=null,n.reset=function(){n.subscription&&n.subscription.dispose(),n.blueprint=new e(window.stackdio.blueprintId,n),n.blueprint.waiting.done(function(){document.title="stackd.io | Blueprint Detail - "+n.blueprint.title()}).fail(function(){window.location="/blueprints/"});var t=i(".checkbox-custom");n.subscription=n.blueprint.createUsers.subscribe(function(i){i?t.checkbox("check"):t.checkbox("uncheck")})},n.reset()}});