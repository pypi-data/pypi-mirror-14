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

define(["bootbox","utils/bootstrap-growl"],function(r){"use strict";return{addError:function(r,e){var a=$(r);a.addClass("has-error"),e.forEach(function(r){a.append('<span class="help-block">'+r+"</span>")})},growlAlert:function(r,e){$.bootstrapGrowl(r,{ele:"#main-content",width:"450px",type:e})},alertError:function(e,a,s){var t;try{var o=JSON.parse(e.responseText);t="";for(var n in o)if(o.hasOwnProperty(n)){var i=n.replace("_"," ");o[n].forEach(function(r){t+="<dt>"+i+"</dt><dd>"+r+"</dd>"})}t='<dl class="dl-horizontal">'+t+"</dl>",s&&(t=s+t)}catch(l){t="Oops... there was a server error.  This has been reported to your administrators."}r.alert({title:a,message:t})},parseSaveError:function(e,a,s){var t="";try{var o=JSON.parse(e.responseText);for(var n in o)if(o.hasOwnProperty(n))if(s.indexOf(n)>=0){var i=$("#"+n);i.addClass("has-error"),o[n].forEach(function(r){i.append('<span class="help-block">'+r+"</span>")})}else if("non_field_errors"===n)o[n].forEach(function(r){if(r.indexOf("title")>=0){var e=$("#title");e.addClass("has-error"),e.append('<span class="help-block">A '+a+" with this title already exists.</span>")}});else{var l=n.replace("_"," ");o[n].forEach(function(r){t+="<dt>"+l+"</dt><dd>"+r+"</dd>"})}t&&(t='<dl class="dl-horizontal">'+t+"</dl>")}catch(d){t="Oops... there was a server error.  This has been reported to your administrators."}t&&r.alert({title:"Error saving "+a,message:t})}}});