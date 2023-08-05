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

define(["jquery","knockout","bootbox","generics/pagination","models/stack","models/host"],function(e,t,n,r,i,s){"use strict";return r.extend({breadcrumbs:[{active:!1,title:"Stacks",href:"/stacks/"},{active:!1,title:window.stackdio.stackTitle,href:"/stacks/"+window.stackdio.stackId+"/"},{active:!0,title:"Hosts"}],stack:t.observable(),autoRefresh:!0,model:s,baseUrl:"/stacks/",initialUrl:"/api/stacks/"+window.stackdio.stackId+"/hosts/",sortableFields:[{name:"hostDefinition",displayName:"Host Type",width:"15%"},{name:"hostname",displayName:"Hostname",width:"15%"},{name:"fqdn",displayName:"FQDN",width:"30%"},{name:"privateDNS",displayName:"Private DNS",width:"15%"},{name:"publicDNS",displayName:"Public DNS",width:"15%"},{name:"state",displayName:"State",width:"10%"}],selectedHostDef:t.observable(null),selectedAction:t.observable(null),actionCount:t.observable(1),actions:["add","remove"],init:function(){this._super(),this.stack(new i(window.stackdio.stackId,this));var e=this;this.stack().waiting.done(function(){e.stack().loadBlueprint().done(function(){e.stack().blueprint().loadHostDefinitions()})}),this.hostDefinitions=t.computed(function(){return e.stack().blueprint()?e.stack().blueprint().hostDefinitions():[]})},addRemoveHosts:function(){var e,t,r,i,s=!1;try{i=parseInt(this.actionCount())}catch(o){s=!0}i<1&&(s=!0);if(s){n.alert({title:"Error adding or removing hosts",message:"The count of hosts must be a positive non-zero integer."});return}var u=this.selectedHostDef(),a=i===1?"":"s";switch(this.selectedAction()){case"add":e=this.stack().addHosts,t="Add "+i+" host"+a+" to stack",r="Are you sure you want to add "+i+" <strong>"+u.title()+"</strong> host"+a+" to "+"<strong>"+this.stack().title()+"</strong>?";break;case"remove":e=this.stack().removeHosts,t="Remove "+i+" host"+a+" from stack",r="Are you sure you want to remove "+i+" <strong>"+u.title()+"</strong> host"+a+" from "+"<strong>"+this.stack().title()+"</strong>?";break;default:}var f=this;n.confirm({title:t,message:r,callback:function(t){t&&e.call(f.stack(),u,i)}})}})});