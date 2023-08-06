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

define(["jquery","knockout","bootbox","utils/utils","utils/formula-versions","generics/pagination","models/formula-version"],function(e,r,s,o,t,i,a){"use strict";return i.extend({objectId:null,parentModel:null,parentObject:r.observable(),formulas:null,autoRefresh:!1,model:a,baseUrl:null,initialUrl:null,versionsReady:r.observable(!window.stackdio.hasUpdatePerm),sortableFields:[{name:"formula",displayName:"Formula",width:"60%"},{name:"version",displayName:"Version",width:"40%"}],init:function(){this._super(),this.parentObject(new this.parentModel(this.objectId,this))},createSelectors:function(){var e=this,r=[];this.objects().forEach(function(s){t.createVersionSelector(s,e.formulas)||r.push(s)}),r.forEach(function(r){e.objects.remove(r)}),this.versionsReady(!0)},extraReloadSteps:function(){if(window.stackdio.hasUpdatePerm)if(this.formulas)this.createSelectors();else{var e=this;t.getAllFormulas(function(r){e.formulas=r,e.createSelectors()})}},saveVersions:function(){var r=[],s=this;this.objects().forEach(function(t){r.push(e.ajax({method:"POST",url:s.parentObject().raw.formula_versions,data:JSON.stringify({formula:t.formula(),version:t.version()})}).fail(function(e){o.alertError(e,"Error saving formula version","Errors saving version for "+t.formula()+":<br>")}))}),e.when.apply(this,r).done(function(){o.growlAlert("Successfully saved formula versions.","success")})}})});