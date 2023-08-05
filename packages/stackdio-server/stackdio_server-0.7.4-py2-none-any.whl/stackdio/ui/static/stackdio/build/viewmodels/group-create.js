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

define(["jquery","knockout","ladda","bootbox"],function(e,t,n,r){"use strict";return function(){var i=this;i.breadcrumbs=[{active:!1,title:"Groups",href:"/groups/"},{active:!0,title:"New"}],i.name=t.observable(),i.reset=function(){i.name("")},i.removeErrors=function(t){t.forEach(function(t){var n=e("#"+t);n.removeClass("has-error");var r=n.find(".help-block");r.remove()})},i.createGroup=function(){var t=["name"];i.removeErrors(t);var s=n.create(document.querySelector("#create-button"));s.start(),e.ajax({method:"POST",url:"/api/groups/",data:JSON.stringify({name:i.name()})}).always(function(){s.stop()}).done(function(e){window.location="/groups/"+e.name+"/members/"}).fail(function(n){var i="";try{var s=JSON.parse(n.responseText);for(var o in s)if(s.hasOwnProperty(o))if(t.indexOf(o)>=0){var u=e("#"+o);u.addClass("has-error"),s[o].forEach(function(e){u.append('<span class="help-block">'+e+"</span>")})}else if(o==="non_field_errors")s[o].forEach(function(t){if(t.indexOf("name")>=0){var n=e("#name");n.addClass("has-error"),n.append('<span class="help-block">A group with this name already exists.</span>')}});else{var a=o.replace("_"," ");s[o].forEach(function(e){i+="<dt>"+a+"</dt><dd>"+e+"</dd>"})}i&&(i='<dl class="dl-horizontal">'+i+"</dl>")}catch(f){i="Oops... there was a server error.  This has been reported to your administrators."}i&&r.alert({title:"Error creating group",message:i})})},i.reset()}});