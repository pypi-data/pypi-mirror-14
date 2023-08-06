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

define(["jquery","generics/pagination","models/stack"],function(t,a,e){"use strict";return a.extend({breadcrumbs:[{active:!0,title:"Stacks"}],model:e,baseUrl:"/stacks/",initialUrl:"/api/stacks/",sortableFields:[{name:"title",displayName:"Title",width:"15%"},{name:"description",displayName:"Description",width:"20%"},{name:"namespace",displayName:"Namespace",width:"15%"},{name:"created",displayName:"Launched",width:"15%"},{name:"hostCount",displayName:"Hosts",width:"10%"},{name:"status",displayName:"Status",width:"10%"}],openActionStackId:null,actionMap:{},reset:function(){this.openActionStackId=null,this.actionMap={},this._super()},processObject:function(t){this.actionMap.hasOwnProperty(t.id)&&t.availableActions(this.actionMap[t.id])},extraReloadSteps:function(){var a=t(".action-dropdown"),e=this;a.on("show.bs.dropdown",function(t){var a=parseInt(t.target.id);e.openActionStackId=a;for(var i=e.objects(),n=0,s=i.length;s>n;++n)if(i[n].id===a){i[n].loadAvailableActions();break}}),a.on("hide.bs.dropdown",function(){e.openActionStackId=null})}})});