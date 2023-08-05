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

define(["jquery","knockout","generics/pagination","utils/utils","models/security-group","select2"],function(e,t,n,r,i){"use strict";return n.extend({breadcrumbs:[{active:!1,title:"Cloud Accounts",href:"/accounts/"},{active:!1,title:window.stackdio.accountTitle,href:"/accounts/"+window.stackdio.accountId+"/"},{active:!0,title:"Default Security Groups"}],model:i,newGroupName:t.observable(),baseUrl:"/accounts/"+window.stackdio.accountId+"/security_groups/",accountUrl:"/api/cloud/accounts/"+window.stackdio.accountId+"/",initialUrl:"/api/cloud/accounts/"+window.stackdio.accountId+"/security_groups/",sortableFields:[{name:"name",displayName:"Name",width:"30%"},{name:"description",displayName:"Description",width:"35%"},{name:"managed",displayName:"Managed",width:"10%"},{name:"groupId",displayName:"Group ID",width:"15%"}],filterObject:function(e){return e.default},init:function(){this._super(),this.createSelector();var t=this;this.sgSelector.on("select2:select",function(n){var i=n.params.data;e.ajax({method:"POST",url:t.accountUrl+"security_groups/",data:JSON.stringify({group_id:i.group_id,"default":!0})}).done(function(){t.sgSelector.empty(),t.sgSelector.val(null).trigger("change"),t.reload()}).fail(function(e){r.alertError(e,"Error saving permissions")})})},createSelector:function(){this.sgSelector=e("#accountSecurityGroups");var t=this;this.sgSelector.select2({ajax:{url:this.accountUrl+"security_groups/all/",dataType:"json",delay:100,data:function(e){return{name:e.term}},processResults:function(e){var n=[];return e.results.forEach(function(e){e.text=e.name,e.id=e.name;var r=!0;t.objects().forEach(function(t){t.groupId()===e.group_id&&(r=!1)}),r&&n.push(e)}),{results:n}},cache:!0},theme:"bootstrap",disabled:!1,placeholder:"Select a security group...",minimumInputLength:0})},addNewGroup:function(){var t=this;e.ajax({method:"POST",url:this.accountUrl+"security_groups/",data:JSON.stringify({name:this.newGroupName(),"default":!0})}).done(function(){t.newGroupName(""),t.reload()}).fail(function(e){r.alertError(e,"Error saving permissions")})}})});