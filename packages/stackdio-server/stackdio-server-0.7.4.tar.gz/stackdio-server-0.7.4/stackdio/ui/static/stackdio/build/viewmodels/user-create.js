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

define(["jquery","knockout","ladda","bootbox"],function(e,t,n,r){"use strict";return function(){var i=this;i.breadcrumbs=[{active:!1,title:"Users",href:"/users/"},{active:!0,title:"New"}],i.username=t.observable(),i.firstName=t.observable(),i.lastName=t.observable(),i.email=t.observable(),i.reset=function(){i.username(""),i.firstName(""),i.lastName(""),i.email("")},i.removeErrors=function(t){t.forEach(function(t){var n=e("#"+t);n.removeClass("has-error");var r=n.find(".help-block");r.remove()})},i.createUser=function(){var t=i.username();r.confirm({title:"Confirm user creation",message:"Are you sure you want to create <strong>"+t+"</strong>?<br>"+"An email <strong>will</strong> be sent to the provided email address.",buttons:{confirm:{label:"Create",className:"btn-primary"}},callback:function(t){if(t){var s=["username","first_name","last_name","email"];i.removeErrors(s);var o=n.create(document.querySelector("#create-button"));o.start(),e.ajax({method:"POST",url:"/api/users/",data:JSON.stringify({username:i.username(),first_name:i.firstName(),last_name:i.lastName(),email:i.email()})}).always(function(){o.stop()}).done(function(){window.location="/users/"}).fail(function(t){var n="";try{var i=JSON.parse(t.responseText);for(var o in i)if(i.hasOwnProperty(o))if(s.indexOf(o)>=0){var u=e("#"+o);u.addClass("has-error"),i[o].forEach(function(e){u.append('<span class="help-block">'+e+"</span>")})}else if(o==="non_field_errors")i[o].forEach(function(t){if(t.indexOf("username")>=0){var n=e("#username");n.addClass("has-error"),n.append('<span class="help-block">A user with this username already exists.</span>')}});else{var a=o.replace("_"," ");i[o].forEach(function(e){n+="<dt>"+a+"</dt><dd>"+e+"</dd>"})}n&&(n='<dl class="dl-horizontal">'+n+"</dl>")}catch(f){n="Oops... there was a server error.  This has been reported to your administrators."}n&&r.alert({title:"Error creating user",message:n})})}}})},i.reset()}});