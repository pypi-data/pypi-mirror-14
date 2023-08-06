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

define(["jquery","knockout","ladda","bootbox"],function(e,r,a,s){"use strict";return function(){var t=this;t.breadcrumbs=[{active:!1,title:"Users",href:"/users/"},{active:!0,title:"New"}],t.username=r.observable(),t.firstName=r.observable(),t.lastName=r.observable(),t.email=r.observable(),t.reset=function(){t.username(""),t.firstName(""),t.lastName(""),t.email("")},t.removeErrors=function(r){r.forEach(function(r){var a=e("#"+r);a.removeClass("has-error");var s=a.find(".help-block");s.remove()})},t.createUser=function(){var r=t.username();s.confirm({title:"Confirm user creation",message:"Are you sure you want to create <strong>"+r+"</strong>?<br>An email <strong>will</strong> be sent to the provided email address.",buttons:{confirm:{label:"Create",className:"btn-primary"}},callback:function(r){if(r){var n=["username","first_name","last_name","email"];t.removeErrors(n);var o=a.create(document.querySelector("#create-button"));o.start(),e.ajax({method:"POST",url:"/api/users/",data:JSON.stringify({username:t.username(),first_name:t.firstName(),last_name:t.lastName(),email:t.email()})}).always(function(){o.stop()}).done(function(){window.location="/users/"}).fail(function(r){var a="";try{var t=JSON.parse(r.responseText);for(var o in t)if(t.hasOwnProperty(o))if(n.indexOf(o)>=0){var i=e("#"+o);i.addClass("has-error"),t[o].forEach(function(e){i.append('<span class="help-block">'+e+"</span>")})}else if("non_field_errors"===o)t[o].forEach(function(r){if(r.indexOf("username")>=0){var a=e("#username");a.addClass("has-error"),a.append('<span class="help-block">A user with this username already exists.</span>')}});else{var l=o.replace("_"," ");t[o].forEach(function(e){a+="<dt>"+l+"</dt><dd>"+e+"</dd>"})}a&&(a='<dl class="dl-horizontal">'+a+"</dl>")}catch(c){a="Oops... there was a server error.  This has been reported to your administrators."}a&&s.alert({title:"Error creating user",message:a})})}}})},t.reset()}});