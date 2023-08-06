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

define(["jquery","knockout","bootbox","generics/pagination","models/stack","models/host"],function(t,s,e,i,o,a){"use strict";return i.extend({breadcrumbs:[{active:!1,title:"Stacks",href:"/stacks/"},{active:!1,title:window.stackdio.stackTitle,href:"/stacks/"+window.stackdio.stackId+"/"},{active:!0,title:"Hosts"}],stack:s.observable(),autoRefresh:!0,model:a,baseUrl:"/stacks/",initialUrl:"/api/stacks/"+window.stackdio.stackId+"/hosts/",sortableFields:[{name:"hostDefinition",displayName:"Host Type",width:"15%"},{name:"hostname",displayName:"Hostname",width:"15%"},{name:"fqdn",displayName:"FQDN",width:"30%"},{name:"privateDNS",displayName:"Private DNS",width:"15%"},{name:"publicDNS",displayName:"Public DNS",width:"15%"},{name:"state",displayName:"State",width:"10%"}],selectedHostDef:s.observable(null),selectedAction:s.observable(null),actionCount:s.observable(1),actions:["add","remove"],init:function(){this._super(),this.stack(new o(window.stackdio.stackId,this));var t=this;this.stack().waiting.done(function(){t.stack().loadBlueprint().done(function(){t.stack().blueprint().loadHostDefinitions()})}),this.hostDefinitions=s.computed(function(){return t.stack().blueprint()?t.stack().blueprint().hostDefinitions():[]})},addRemoveHosts:function(){var t,s,i,o,a=!1;try{o=parseInt(this.actionCount())}catch(n){a=!0}if(1>o&&(a=!0),a)return void e.alert({title:"Error adding or removing hosts",message:"The count of hosts must be a positive non-zero integer."});var c=this.selectedHostDef(),r=1===o?"":"s";switch(this.selectedAction()){case"add":t=this.stack().addHosts,s="Add "+o+" host"+r+" to stack",i="Are you sure you want to add "+o+" <strong>"+c.title()+"</strong> host"+r+" to <strong>"+this.stack().title()+"</strong>?";break;case"remove":t=this.stack().removeHosts,s="Remove "+o+" host"+r+" from stack",i="Are you sure you want to remove "+o+" <strong>"+c.title()+"</strong> host"+r+" from <strong>"+this.stack().title()+"</strong>?"}var d=this;e.confirm({title:s,message:i,callback:function(s){s&&t.call(d.stack(),c,o)}})}})});