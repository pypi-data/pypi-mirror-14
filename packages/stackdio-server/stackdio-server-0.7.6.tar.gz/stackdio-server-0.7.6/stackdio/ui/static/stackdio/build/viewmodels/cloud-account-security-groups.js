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

define(["jquery","knockout","generics/pagination","utils/utils","models/security-group","select2"],function(t,e,a,r,i){"use strict";return a.extend({breadcrumbs:[{active:!1,title:"Cloud Accounts",href:"/accounts/"},{active:!1,title:window.stackdio.accountTitle,href:"/accounts/"+window.stackdio.accountId+"/"},{active:!0,title:"Default Security Groups"}],model:i,newGroupName:e.observable(),baseUrl:"/accounts/"+window.stackdio.accountId+"/security_groups/",accountUrl:"/api/cloud/accounts/"+window.stackdio.accountId+"/",initialUrl:"/api/cloud/accounts/"+window.stackdio.accountId+"/security_groups/",sortableFields:[{name:"name",displayName:"Name",width:"30%"},{name:"description",displayName:"Description",width:"35%"},{name:"managed",displayName:"Managed",width:"10%"},{name:"groupId",displayName:"Group ID",width:"15%"}],filterObject:function(t){return t["default"]},init:function(){this._super(),this.createSelector();var e=this;this.sgSelector.on("select2:select",function(a){var i=a.params.data;t.ajax({method:"POST",url:e.accountUrl+"security_groups/",data:JSON.stringify({group_id:i.group_id,"default":!0})}).done(function(){e.sgSelector.empty(),e.sgSelector.val(null).trigger("change"),e.reload()}).fail(function(t){r.alertError(t,"Error saving permissions")})})},createSelector:function(){this.sgSelector=t("#accountSecurityGroups");var e=this;this.sgSelector.select2({ajax:{url:this.accountUrl+"security_groups/all/",dataType:"json",delay:100,data:function(t){return{name:t.term}},processResults:function(t){var a=[];return t.results.forEach(function(t){t.text=t.name,t.id=t.name;var r=!0;e.objects().forEach(function(e){e.groupId()===t.group_id&&(r=!1)}),r&&a.push(t)}),{results:a}},cache:!0},theme:"bootstrap",disabled:!1,placeholder:"Select a security group...",minimumInputLength:0})},addNewGroup:function(){var e=this;t.ajax({method:"POST",url:this.accountUrl+"security_groups/",data:JSON.stringify({name:this.newGroupName(),"default":!0})}).done(function(){e.newGroupName(""),e.reload()}).fail(function(t){r.alertError(t,"Error saving permissions")})}})});