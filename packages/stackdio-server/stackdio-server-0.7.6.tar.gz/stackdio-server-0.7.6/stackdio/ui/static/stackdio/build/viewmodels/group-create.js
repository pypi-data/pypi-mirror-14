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

define(["jquery","knockout","ladda","bootbox"],function(e,r,a,o){"use strict";return function(){var n=this;n.breadcrumbs=[{active:!1,title:"Groups",href:"/groups/"},{active:!0,title:"New"}],n.name=r.observable(),n.reset=function(){n.name("")},n.removeErrors=function(r){r.forEach(function(r){var a=e("#"+r);a.removeClass("has-error");var o=a.find(".help-block");o.remove()})},n.createGroup=function(){var r=["name"];n.removeErrors(r);var t=a.create(document.querySelector("#create-button"));t.start(),e.ajax({method:"POST",url:"/api/groups/",data:JSON.stringify({name:n.name()})}).always(function(){t.stop()}).done(function(e){window.location="/groups/"+e.name+"/members/"}).fail(function(a){var n="";try{var t=JSON.parse(a.responseText);for(var s in t)if(t.hasOwnProperty(s))if(r.indexOf(s)>=0){var i=e("#"+s);i.addClass("has-error"),t[s].forEach(function(e){i.append('<span class="help-block">'+e+"</span>")})}else if("non_field_errors"===s)t[s].forEach(function(r){if(r.indexOf("name")>=0){var a=e("#name");a.addClass("has-error"),a.append('<span class="help-block">A group with this name already exists.</span>')}});else{var c=s.replace("_"," ");t[s].forEach(function(e){n+="<dt>"+c+"</dt><dd>"+e+"</dd>"})}n&&(n='<dl class="dl-horizontal">'+n+"</dl>")}catch(l){n="Oops... there was a server error.  This has been reported to your administrators."}n&&o.alert({title:"Error creating group",message:n})})},n.reset()}});