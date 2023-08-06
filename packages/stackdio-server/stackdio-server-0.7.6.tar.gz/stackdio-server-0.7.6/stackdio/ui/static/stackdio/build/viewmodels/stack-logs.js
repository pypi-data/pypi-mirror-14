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

define(["jquery","knockout","bootbox","utils/utils","models/stack","fuelux"],function(t,e,l,o,a){"use strict";return function(){var l=this;l.breadcrumbs=[{active:!1,title:"Stacks",href:"/stacks/"},{active:!1,title:window.stackdio.stackTitle,href:"/stacks/"+window.stackdio.stackId+"/"},{active:!0,title:"Logs"}],l.selectedLogUrl=null,l.log=e.observable(),l.stack=e.observable(),l.reset=function(){l.stack(new a(window.stackdio.stackId,l)),l.selectedLogUrl=null,l.log("Select a log...")},l.reload=function(e){"undefined"==typeof e&&(e=!1),l.selectedLogUrl&&(e&&l.log("Loading..."),t.ajax({method:"GET",url:l.selectedLogUrl,headers:{Accept:"text/plain"}}).done(function(t){var o=document.getElementById("log-text"),a=o.scrollTop,r=o.scrollHeight;l.log(t),(550>r-a||e)&&(o.scrollTop=o.scrollHeight-498)}).fail(function(t){403==t.status?window.location.reload(!0):o.growlAlert("Failed to load log","danger")}))},l.dataSource=function(t,e){var o;"Latest"===t.text?o=l.stack().latestLogs():"Historical"===t.text?o=l.stack().historicalLogs():(l.stack().loadLogs(),o=[{text:"Latest",type:"folder"},{text:"Historical",type:"folder"}]),e({data:o})},l.reset();var r=t("#log-selector");r.tree({dataSource:l.dataSource,cacheItems:!1,folderSelect:!1}),l.intervalId=null,r.on("selected.fu.tree",function(t,e){l.selectedLogUrl=e.target.url,clearInterval(l.intervalId),l.reload(!0),e.target.url.indexOf("latest")>=0&&(l.intervalId=setInterval(l.reload,3e3))})}});