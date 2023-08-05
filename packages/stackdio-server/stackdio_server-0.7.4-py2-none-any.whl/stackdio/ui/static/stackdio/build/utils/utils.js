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

define(["bootbox","utils/bootstrap-growl"],function(e){"use strict";return{addError:function(e,t){var n=$(e);n.addClass("has-error"),t.forEach(function(e){n.append('<span class="help-block">'+e+"</span>")})},growlAlert:function(e,t){$.bootstrapGrowl(e,{ele:"#main-content",width:"450px",type:t})},alertError:function(t,n,r){var i;try{var s=JSON.parse(t.responseText);i="";for(var o in s)if(s.hasOwnProperty(o)){var u=o.replace("_"," ");s[o].forEach(function(e){i+="<dt>"+u+"</dt><dd>"+e+"</dd>"})}i='<dl class="dl-horizontal">'+i+"</dl>",r&&(i=r+i)}catch(a){i="Oops... there was a server error.  This has been reported to your administrators."}e.alert({title:n,message:i})},parseSaveError:function(t,n,r){var i="";try{var s=JSON.parse(t.responseText);for(var o in s)if(s.hasOwnProperty(o))if(r.indexOf(o)>=0){var u=$("#"+o);u.addClass("has-error"),s[o].forEach(function(e){u.append('<span class="help-block">'+e+"</span>")})}else if(o==="non_field_errors")s[o].forEach(function(e){if(e.indexOf("title")>=0){var t=$("#title");t.addClass("has-error"),t.append('<span class="help-block">A '+n+" with this title already exists.</span>")}});else{var a=o.replace("_"," ");s[o].forEach(function(e){i+="<dt>"+a+"</dt><dd>"+e+"</dd>"})}i&&(i='<dl class="dl-horizontal">'+i+"</dl>")}catch(f){i="Oops... there was a server error.  This has been reported to your administrators."}i&&e.alert({title:"Error saving "+n,message:i})}}});