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

define(["jquery","knockout","bootbox"],function(e,t,n){"use strict";return function(){var r=this;r.breadcrumbs=[{active:!1,title:"Profile",href:"/user/"},{active:!0,title:"Change Password"}],r.currentPassword=t.observable(),r.newPassword1=t.observable(),r.newPassword2=t.observable(),r.reset=function(){r.currentPassword(""),r.newPassword1(""),r.newPassword2("")},r.removeErrors=function(t){t.forEach(function(t){var n=e("#"+t);n.removeClass("has-error");var r=n.find(".help-block");r.remove()})},r.changePassword=function(){var t=["current_password","new_password1","new_password2"];r.removeErrors(t),e.ajax({method:"POST",url:"/api/user/password/",data:JSON.stringify({current_password:r.currentPassword(),new_password1:r.newPassword1(),new_password2:r.newPassword2()})}).done(function(){window.location="/user/"}).fail(function(r){var i="";try{var s=JSON.parse(r.responseText);for(var o in s)if(s.hasOwnProperty(o))if(t.indexOf(o)>=0){var u=e("#"+o);u.addClass("has-error"),s[o].forEach(function(e){u.append('<span class="help-block">'+e+"</span>")})}else{var a=o.replace("_"," ");s[o].forEach(function(e){i+="<dt>"+a+"</dt><dd>"+e+"</dd>"})}i&&(i='<dl class="dl-horizontal">'+i+"</dl>")}catch(f){i="Oops... there was a server error.  This has been reported to your administrators."}i&&n.alert({title:"Error changing password",message:i})})},r.reset()}});