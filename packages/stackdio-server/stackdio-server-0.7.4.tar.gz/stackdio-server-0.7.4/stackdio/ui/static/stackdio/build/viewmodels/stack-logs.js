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

define(["jquery","knockout","bootbox","utils/utils","models/stack","fuelux"],function(e,t,n,r,i){"use strict";return function(){var n=this;n.breadcrumbs=[{active:!1,title:"Stacks",href:"/stacks/"},{active:!1,title:window.stackdio.stackTitle,href:"/stacks/"+window.stackdio.stackId+"/"},{active:!0,title:"Logs"}],n.selectedLogUrl=null,n.log=t.observable(),n.stack=t.observable(),n.reset=function(){n.stack(new i(window.stackdio.stackId,n)),n.selectedLogUrl=null,n.log("Select a log...")},n.reload=function(t){typeof t=="undefined"&&(t=!1),n.selectedLogUrl&&(t&&n.log("Loading..."),e.ajax({method:"GET",url:n.selectedLogUrl,headers:{Accept:"text/plain"}}).done(function(e){var r=document.getElementById("log-text"),i=r.scrollTop,s=r.scrollHeight;n.log(e);if(s-i<550||t)r.scrollTop=r.scrollHeight-498}).fail(function(e){e.status==403?window.location.reload(!0):r.growlAlert("Failed to load log","danger")}))},n.dataSource=function(e,t){var r;e.text==="Latest"?r=n.stack().latestLogs():e.text==="Historical"?r=n.stack().historicalLogs():(n.stack().loadLogs(),r=[{text:"Latest",type:"folder"},{text:"Historical",type:"folder"}]),t({data:r})},n.reset();var s=e("#log-selector");s.tree({dataSource:n.dataSource,cacheItems:!1,folderSelect:!1}),n.intervalId=null,s.on("selected.fu.tree",function(e,t){n.selectedLogUrl=t.target.url,clearInterval(n.intervalId),n.reload(!0),t.target.url.indexOf("latest")>=0&&(n.intervalId=setInterval(n.reload,3e3))})}});