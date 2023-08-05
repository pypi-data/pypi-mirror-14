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

define(["jquery","knockout","bootbox","utils/utils","utils/formula-versions","generics/pagination","models/formula-version"],function(e,t,n,r,i,s,o){"use strict";return s.extend({objectId:null,parentModel:null,parentObject:t.observable(),formulas:null,autoRefresh:!1,model:o,baseUrl:null,initialUrl:null,versionsReady:t.observable(!window.stackdio.hasUpdatePerm),sortableFields:[{name:"formula",displayName:"Formula",width:"60%"},{name:"version",displayName:"Version",width:"40%"}],init:function(){this._super(),this.parentObject(new this.parentModel(this.objectId,this))},createSelectors:function(){var e=this,t=[];this.objects().forEach(function(n){i.createVersionSelector(n,e.formulas)||t.push(n)}),t.forEach(function(t){e.objects.remove(t)}),this.versionsReady(!0)},extraReloadSteps:function(){if(window.stackdio.hasUpdatePerm)if(this.formulas)this.createSelectors();else{var e=this;i.getAllFormulas(function(t){e.formulas=t,e.createSelectors()})}},saveVersions:function(){var t=[],n=this;this.objects().forEach(function(i){t.push(e.ajax({method:"POST",url:n.parentObject().raw.formula_versions,data:JSON.stringify({formula:i.formula(),version:i.version()})}).fail(function(e){r.alertError(e,"Error saving formula version","Errors saving version for "+i.formula()+":<br>")}))}),e.when.apply(this,t).done(function(){r.growlAlert("Successfully saved formula versions.","success")})}})});