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

define(["jquery","knockout","models/stack"],function(t,c,i){"use strict";return function(){var s=this;s.stack=null,s.blueprintTitle=c.observable(window.stackdio.blueprintTitle),s.blueprintUrl=c.observable("/blueprints/"+window.stackdio.blueprintId+"/"),s.breadcrumbs=[{active:!1,title:"Stacks",href:"/stacks/"},{active:!0,title:window.stackdio.stackTitle}],s.subscription=null,s.reset=function(){s.subscription&&s.subscription.dispose(),s.stack=new i(window.stackdio.stackId,s),s.stack.waiting.done(function(){document.title="stackd.io | Stack Detail - "+s.stack.title()}).fail(function(){window.location="/stacks/"});var c=t(".checkbox-custom");s.subscription=s.stack.createUsers.subscribe(function(t){t?c.checkbox("check"):c.checkbox("uncheck")})},s.refreshStack=function(){s.stack.refreshStatus().fail(function(){window.location="/stacks/"}),s.stack.loadHistory()},t(".action-dropdown").on("show.bs.dropdown",function(){s.stack.loadAvailableActions()}),s.reset(),s.refreshStack(),setInterval(s.refreshStack,3e3)}});