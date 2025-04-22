<template>
    <el-container>
        <el-header>
            <el-row type="flex" justify="space-between" align="middle">
                <el-col :span="24" style="text-align: right;">
                  <div class="header-buttons">
                    <el-button circle icon="el-icon-setting" @click="settingVisble=true"></el-button>
                    <el-button circle icon="el-icon-question" @click="introVisble=true"></el-button>
                    <el-link :underline="false" href="https://github.com/QuantAskk/pokemonle" style="margin-left:10px">
                        <el-button circle icon="el-icon-user"></el-button>
                    </el-link>
                  </div>
                </el-col>
            </el-row>

            <el-dialog
                title="设置"
                :visible.sync="settingVisble"
                :width="isMobile ? '90%' : '50%'"
                :show-close="false"
                :close-on-click-modal="false"
                :close-on-press-escape="false">
                <div class="setting">
                    模式：<el-select v-model="settings.hardid" placeholder="请选择" size="small" style="width: 50%">
                        <el-option
                        v-for="item in this.hards"
                        :key="item"
                        :label="item"
                        :value="item"
                        >
                        </el-option>
                    </el-select>
                    <br>
                    世代：<el-select v-model="settings.genid" placeholder="请选择" size="small" style="width: 50%"
                        @change="ReloadGuessNumber()">
                        <el-option
                        v-for="item in this.gens"
                        :key="item"
                        :label="item"
                        :value="item"
                        >
                        </el-option>
                    </el-select>
                    <br>
                    <el-switch
                    v-model="settings.battleOpen"
                    active-text="显示更多种族值信息"
                    @change="ReloadGuessNumber()">
                    </el-switch>
                    <el-switch
                    v-model="settings.shapeOpen"
                    active-text="显示更多外形信息"
                    @change="ReloadGuessNumber()">
                    </el-switch>
                    <el-switch
                    v-model="settings.catchOpen"
                    active-text="显示蛋组/捕获率信息"
                    @change="ReloadGuessNumber()">
                    </el-switch>
                    <br>
                    <el-switch
                    v-model="settings.autodif"
                    active-text="自动调整"
                    inactive-text="手动调整"
                    @change="ReloadGuessNumber()">
                    </el-switch>
                    <div class="block">
                        <span class="demonstration">猜测次数：{{this.settings.maxguess}}</span>
                        <el-slider
                        v-model="settings.maxguess"
                        :step="1"
                        :max="12"
                        :min="2"
                        :disabled="this.settings.autodif"
                        style="width: 100%">
                        </el-slider>
                    </div>
                </div>
                
                <span slot="footer" class="dialog-footer">
                    <el-button type="primary" @click="CloseSetting()">确 定</el-button>
                </span>
            </el-dialog>

            <el-dialog
                title="规则介绍"
                :visible.sync="introVisble"
                :width="isMobile ? '90%' : '50%'"
                :show-close=false>
                <div class="setting">
                    输入一个宝可梦进行猜测。
                    <br>
                    每次猜测后，你会获得你输入的宝可梦的信息。
                    <br>
                    <div>
                        <el-tag type="success" size="small">
                            绿色高亮
                        </el-tag>
                        表示该信息与你需要猜测的宝可梦完全相同；
                    </div>
                    <div>
                        <el-tag type="warning" size="small">
                            黄色高亮
                        </el-tag>
                        表示该信息与你需要猜测的宝可梦比较接近；
                    </div>
                    "↑": 应该往高了猜；"↓": 应该往低了猜；
                    <br>
                    简单模式只会保留较为热门或携带其他标签的宝可梦。
                </div>
                
                <span slot="footer" class="dialog-footer">
                    <el-button type="primary" @click="introVisble=false">确 定</el-button>
                </span>
            </el-dialog>

        </el-header>
        <el-main>
            <div class="guess">
                <!-- 统一居中的输入区域 -->
                <div class="input-container">
                    <el-row type="flex" justify="center" align="middle" class="input-row">
                        <el-col :span="isMobile ? 24 : 12" class="input-col">
                            <el-autocomplete
                            class="inline-input"
                            v-model="input"
                            :fetch-suggestions="querySearch"
                            placeholder="请输入宝可梦名称"
                            :trigger-on-focus="false"
                            style="width: 100%"></el-autocomplete>
                        </el-col>
                    </el-row>
                    <el-row type="flex" justify="center" align="middle" :gutter="20" class="button-row">
                        <el-col :span="isMobile ? 12 : 6" class="button-col">
                            <el-button type="primary" class="action-button" :disabled="this.gameover" @click="Guess()">
                                {{ this.gameover ? '已结束' : '确定' }}
                            </el-button>
                        </el-col>
                        <el-col :span="isMobile ? 12 : 6" class="button-col">
                            <el-button type="success" class="action-button" @click="Restart()">重新开始</el-button>
                        </el-col>
                    </el-row>
                </div>
                
                <div class="times">
                    猜测次数：{{this.times}}/{{this.settings.maxguess}}
                </div>
                
                <!-- 移动端卡片垂直布局 -->
                <div v-if="isMobile" class="pokemon-cards mobile-cards">
                    <div v-for="(item, index) in tableData" :key="index" class="pokemon-card">
                        <div class="card-header">
                            <div class="pokemon-image">
                                <el-image style="width: 50px; height: 50px" :src="item.imgUrl" fit="contain"></el-image>
                            </div>
                            <div class="pokemon-name">{{ item.name }}</div>
                        </div>
                        
                        <div class="card-section">
                            <div class="section-title">属性</div>
                            <div class="section-content">
                                <el-tag v-for="(type, idx) in item.type" :key="'type-'+idx" 
                                    size="mini" :type="type.col" class="info-tag">
                                    {{ type.key }}
                                </el-tag>
                            </div>
                        </div>
                        
                        <div class="card-section">
                            <div class="section-title">种族值</div>
                            <div class="section-content">
                                <el-tag size="mini" :type="item.pow.col" class="info-tag">
                                    {{ ValueText(item.pow.key, item.pow.value) }}
                                </el-tag>
                                <el-tag v-if="settings.battleOpen" size="mini" :type="item.speed.col" class="info-tag">
                                    速度:{{ ValueText(item.speed.key, item.speed.value) }}
                                </el-tag>
                            </div>
                        </div>
                        
                        <div v-if="settings.battleOpen" class="card-section">
                            <div class="section-title">攻防</div>
                            <div class="section-content">
                                <el-tag size="mini" :type="item.attack.col" class="info-tag">
                                    {{ item.attack.key }}
                                </el-tag>
                                <el-tag size="mini" :type="item.defense.col" class="info-tag">
                                    {{ item.defense.key }}
                                </el-tag>
                            </div>
                        </div>
                        
                        <div class="card-section">
                            <div class="section-title">世代</div>
                            <div class="section-content">
                                <el-tag size="mini" :type="item.gen.col" class="info-tag">
                                    {{ ValueText(item.gen.key, item.gen.value) }}
                                </el-tag>
                            </div>
                        </div>
                        
                        <div class="card-section">
                            <div class="section-title">特性</div>
                            <div class="section-content">
                                <el-tag v-for="(ability, idx) in item.ability" :key="'ability-'+idx" 
                                    size="mini" :type="ability.col" class="info-tag">
                                    {{ ability.key }}
                                </el-tag>
                            </div>
                        </div>
                        
                        <div class="card-section">
                            <div class="section-title">进化</div>
                            <div class="section-content">
                                <el-tag v-if="item.evo.key != null" size="mini" :type="item.evo.col" class="info-tag">
                                    {{ item.evo.key }}
                                </el-tag>
                                <el-tag size="mini" :type="item.stage.col" class="info-tag">
                                    {{ item.stage.key }}
                                </el-tag>
                            </div>
                        </div>
                        
                        <div v-if="settings.shapeOpen" class="card-section">
                            <div class="section-title">外形</div>
                            <div class="section-content">
                                <el-tag size="mini" :type="item.shape.col" class="info-tag">
                                    {{ item.shape.key }}
                                </el-tag>
                                <el-tag size="mini" :type="item.col.col" class="info-tag">
                                    {{ item.col.key }}
                                </el-tag>
                            </div>
                        </div>
                        
                        <div v-if="settings.catchOpen" class="card-section">
                            <div class="section-title">蛋组/捕获率</div>
                            <div class="section-content">
                                <el-tag v-for="(egg, idx) in item.egg" :key="'egg-'+idx" 
                                    size="mini" :type="egg.col" class="info-tag">
                                    {{ egg.key }}
                                </el-tag>
                                <el-tag size="mini" :type="item.catrate.col" class="info-tag">
                                    捕获率:{{ ValueText(item.catrate.key, item.catrate.value) }}
                                </el-tag>
                            </div>
                        </div>
                        
                        <div class="card-section">
                            <div class="section-title">其他</div>
                            <div class="section-content">
                                <el-tag v-for="(label, idx) in item.label" :key="'label-'+idx" 
                                    size="mini" :type="label.col" class="info-tag">
                                    {{ label.key }}
                                </el-tag>
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- 桌面端卡片水平布局 -->
                <div v-else class="pokemon-cards desktop-cards">
                    <div v-for="(item, index) in tableData" :key="index" class="pokemon-card desktop-card">
                        <div class="card-header">
                            <div class="pokemon-image">
                                <el-image style="width: 60px; height: 60px" :src="item.imgUrl" fit="contain"></el-image>
                            </div>
                            <div class="pokemon-name">{{ item.name }}</div>
                        </div>
                        
                        <div class="desktop-card-content">
                            <div class="desktop-section">
                                <div class="section-title">属性</div>
                                <div class="section-content">
                                    <el-tag v-for="(type, idx) in item.type" :key="'type-'+idx" 
                                        size="small" :type="type.col" class="info-tag">
                                        {{ type.key }}
                                    </el-tag>
                                </div>
                            </div>
                            
                            <div class="desktop-section">
                                <div class="section-title">种族值</div>
                                <div class="section-content">
                                    <el-tag size="small" :type="item.pow.col" class="info-tag">
                                        {{ ValueText(item.pow.key, item.pow.value) }}
                                    </el-tag>
                                    <el-tag v-if="settings.battleOpen" size="small" :type="item.speed.col" class="info-tag">
                                        速度:{{ ValueText(item.speed.key, item.speed.value) }}
                                    </el-tag>
                                </div>
                            </div>
                            
                            <div v-if="settings.battleOpen" class="desktop-section">
                                <div class="section-title">攻防</div>
                                <div class="section-content">
                                    <el-tag size="small" :type="item.attack.col" class="info-tag">
                                        {{ item.attack.key }}
                                    </el-tag>
                                    <el-tag size="small" :type="item.defense.col" class="info-tag">
                                        {{ item.defense.key }}
                                    </el-tag>
                                </div>
                            </div>
                            
                            <div class="desktop-section">
                                <div class="section-title">世代</div>
                                <div class="section-content">
                                    <el-tag size="small" :type="item.gen.col" class="info-tag">
                                        {{ ValueText(item.gen.key, item.gen.value) }}
                                    </el-tag>
                                </div>
                            </div>
                            
                            <div class="desktop-section">
                                <div class="section-title">特性</div>
                                <div class="section-content">
                                    <el-tag v-for="(ability, idx) in item.ability" :key="'ability-'+idx" 
                                        size="small" :type="ability.col" class="info-tag">
                                        {{ ability.key }}
                                    </el-tag>
                                </div>
                            </div>
                            
                            <div class="desktop-section">
                                <div class="section-title">进化</div>
                                <div class="section-content">
                                    <el-tag v-if="item.evo.key != null" size="small" :type="item.evo.col" class="info-tag">
                                        {{ item.evo.key }}
                                    </el-tag>
                                    <el-tag size="small" :type="item.stage.col" class="info-tag">
                                        {{ item.stage.key }}
                                    </el-tag>
                                </div>
                            </div>
                            
                            <div v-if="settings.shapeOpen" class="desktop-section">
                                <div class="section-title">外形</div>
                                <div class="section-content">
                                    <el-tag size="small" :type="item.shape.col" class="info-tag">
                                        {{ item.shape.key }}
                                    </el-tag>
                                    <el-tag size="small" :type="item.col.col" class="info-tag">
                                        {{ item.col.key }}
                                    </el-tag>
                                </div>
                            </div>
                            
                            <div v-if="settings.catchOpen" class="desktop-section">
                                <div class="section-title">蛋组/捕获率</div>
                                <div class="section-content">
                                    <el-tag v-for="(egg, idx) in item.egg" :key="'egg-'+idx" 
                                        size="small" :type="egg.col" class="info-tag">
                                        {{ egg.key }}
                                    </el-tag>
                                    <el-tag size="small" :type="item.catrate.col" class="info-tag">
                                        捕获率:{{ ValueText(item.catrate.key, item.catrate.value) }}
                                    </el-tag>
                                </div>
                            </div>
                            
                            <div class="desktop-section">
                                <div class="section-title">其他</div>
                                <div class="section-content">
                                    <el-tag v-for="(label, idx) in item.label" :key="'label-'+idx" 
                                        size="small" :type="label.col" class="info-tag">
                                        {{ label.key }}
                                    </el-tag>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </el-main>
    </el-container>
</template>
  
<script>
    import axios from 'axios'
    import { MessageBox } from 'element-ui';

    function truncateString(str, maxLength) {
        if (str.length > maxLength) {
            return str.slice(0, maxLength) + '...';
        }
        return str;
    }

    export default{
        data(){
            return{
                input:"",
                tempdata:null,
                nameList:[],
                tableData: [],
                temp:{},
                reply:{},
                times:0,
                gameover:false,
                settingVisble:false,
                introVisble:false,
                gens:["全世代","第一世代","第二世代","第三世代","第四世代","第五世代","第六世代","第七世代","第八世代","第九世代"],
                hards:["普通模式","简单模式"],
                settings:{
                    genid:"全世代",
                    hardid:"普通模式",
                    maxguess:10,
                    autodif:true,
                    battleOpen:false,
                    shapeOpen:false,
                    catchOpen:false,
                },
                windowWidth: window.innerWidth,
                isMobile: window.innerWidth <= 768
            }
        },
        methods:{
            async createFilter(queryString) {
                if (this.nameList.length === 0) {
                    await this.loadName();
                }
                const query = queryString.toLowerCase();
                
                return (item) => {
                    const target = (item.value || '').toLowerCase();
                    let qIndex = 0, tIndex = 0;
                    
                    while (qIndex < query.length && tIndex < target.length) {
                    if (query[qIndex] === target[tIndex]) qIndex++;
                    tIndex++;
                    }
                    return qIndex === query.length;
                };
            },

            querySearch(queryString, cb) {
                Promise.resolve(this.createFilter(queryString)).then(filter => {
                    const results = queryString 
                    ? this.nameList.filter(filter) 
                    : this.nameList;
                    cb(results);
                }).catch(err => {
                    console.error('Filter error:', err);
                    cb([]);
                });
            },
            async loadName(){
                try{
                    const options = {
                        method: 'GET',
                        url: `${process.env.VUE_APP_API_BASE_URL}/nameget`
                    };

                    await axios.request(options).then((response)=>{
                        this.tempdata=response.data
                    }).catch(function (error) {
                        console.error(error);
                    });
                    
                    this.nameList=this.tempdata.map(item=>({value:item}));
                    
                }catch(error){
                    console.error("请求失败",error)
                }
            },
            async Restart(){
                this.times=0
                this.gameover=false
                sessionStorage.removeItem('answer')
                this.tableData=[]
                console.log(`${process.env.VUE_APP_API_BASE_URL}/initget`)
                try{
                    const gen=this.gens.indexOf(this.settings.genid)
                    const dif=this.hards.indexOf(this.settings.hardid)
                    const options = {
                        method: 'GET',
                        url: `${process.env.VUE_APP_API_BASE_URL}/initget`,
                        params:{
                            difficulty:dif,
                            gen:gen
                        }   
                    };

                    await axios.request(options).then((response)=>{
                        this.tempdata=response.data
                        console.log(this.tempdata)
                    }).catch(function (error) {
                        console.error(error);
                    });
                    sessionStorage.setItem('answer',this.tempdata)
                }catch(error){
                    console.error(error)
                }
            },
            async Guess(){
                const answer=sessionStorage.getItem('answer')
                if(answer==null)return;
                try{
                    const options = {
                        method: 'GET',
                        url: `${process.env.VUE_APP_API_BASE_URL}/guess`,
                        params:{
                            answer:answer,
                            guess:this.input
                        }   
                    };
                    await axios.request(options).then((response)=>{
                        this.tempdata=response.data
                    }).catch(function (error) {
                        console.error(error);
                    });

                    const data=this.tempdata
                    if(data=="guess name error"){
                        this.$notify({
                            title: '提交错误',
                            message: '不存在的宝可梦',
                            type: "error"
                        });
                    }else{
                        this.temp={}

                        this.temp.name=data.name
                        this.temp.answer=data.answer

                        // 属性
                        this.temp.type=[]
                        data.type.forEach((type,index)=>{
                            if(type.key!="无"){
                                if(type.value=='True')
                                    this.temp.type.push({key:type.key,col:"success"})
                                else
                                    this.temp.type.push({key:type.key,col:"info"})
                            }
                        })

                        // 种族值
                        this.temp.pow={}
                        this.temp.pow.key=data.pow.key
                        this.temp.pow.value=data.pow.value
                        if(data.pow.value=="equiv")
                            this.temp.pow.col="success"
                        else if(data.pow.dis=="far")
                            this.temp.pow.col="info"
                        else
                            this.temp.pow.col="warning"

                        //速度
                        this.temp.speed={}
                        this.temp.speed.key=data.speed.key
                        this.temp.speed.value=data.speed.value
                        if(data.speed.value=="equiv")
                            this.temp.speed.col="success"
                        else if(data.speed.dis=="far")
                            this.temp.speed.col="info"
                        else
                            this.temp.speed.col="warning"
                        
                        //物特
                        this.temp.attack={}
                        this.temp.attack.key=data.attack.key
                        this.temp.attack.value=data.attack.value
                        if(data.attack.value=='True')
                            this.temp.attack.col="success"
                        else 
                            this.temp.attack.col="info"

                        this.temp.defense={}
                        this.temp.defense.key=data.defense.key
                        this.temp.defense.value=data.defense.value
                        if(data.defense.value=='True')
                            this.temp.defense.col="success"
                        else 
                            this.temp.defense.col="info"

                        // 世代
                        this.temp.gen={}
                        this.temp.gen.key=data.gen.key
                        this.temp.gen.value=data.gen.value
                        if(data.gen.value=='equiv')
                            this.temp.gen.col="success"
                        else 
                            this.temp.gen.col="info"

                        // 特性
                        this.temp.ability=[]
                        data.ability.forEach((ability,index)=>{
                            if(ability.value=='True')
                                this.temp.ability.push({key:ability.key,col:"success"})
                            else
                                this.temp.ability.push({key:ability.key,col:"info"})
                        })

                        // 进化方式
                        this.temp.evo={}
                        this.temp.evo.key=data.evo.key
                        if(this.temp.evo.key!=null)
                            this.temp.evo.key=truncateString(this.temp.evo.key,this.isMobile ? 6 : 12)
                        if(data.evo.value=="far")
                            this.temp.evo.col="info"
                        else if(data.evo.value=="near")
                            this.temp.evo.col="warning"
                        else 
                            this.temp.evo.col="success"
  
                        // 阶段
                        this.temp.stage={}
                        this.temp.stage.key=data.stage.key
                        this.temp.stage.value=data.stage.value
                        if(data.stage.value=='True')
                            this.temp.stage.col="success"
                        else 
                            this.temp.stage.col="info"

                        //蛋组
                        this.temp.egg=[]
                        data.egg.forEach((egg,index)=>{
                            if(egg.value=='True')
                                this.temp.egg.push({key:egg.key,col:"success"})
                            else
                                this.temp.egg.push({key:egg.key,col:"info"})
                        })

                        //捕获率
                        this.temp.catrate={}
                        this.temp.catrate.key=data.catrate.key
                        this.temp.catrate.value=data.catrate.value
                        if(data.catrate.value=="equiv")
                            this.temp.catrate.col="success"
                        else
                            this.temp.catrate.col="info"
                        
                        //外形
                        this.temp.shape={}
                        this.temp.shape.key=data.shape.key
                        this.temp.shape.value=data.shape.value
                        if(data.shape.value=='True')
                            this.temp.shape.col="success"
                        else 
                            this.temp.shape.col="info"

                        this.temp.col={}
                        this.temp.col.key=data.col.key
                        this.temp.col.value=data.col.value
                        if(data.col.value=='True')
                            this.temp.col.col="success"
                        else 
                            this.temp.col.col="info"

                        // 其他标签
                        this.temp.label=[]
                        data.label.forEach((label,index)=>{
                            if(label.value=='True')
                                this.temp.label.push({key:label.key,col:"success"})
                            else
                                this.temp.label.push({key:label.key,col:"info"})
                        })

                        console.log(this.temp)

                        // 获取图片
                        try{
                            const options = {
                                method: 'GET',
                                url: `${process.env.VUE_APP_API_BASE_URL}/getimage`,
                                params: {pokemon: this.temp.name},
                                responseType:'blob'
                            };
                            await axios.request(options).then((response)=>{
                                this.tempdata=response.data
                            }).catch(function (error) {
                                console.error(error);
                            });
                            const blob=new Blob([this.tempdata]);
                            this.temp.imgUrl=URL.createObjectURL(blob);
                        }catch(error){
                            console.error('图片获取失败:',error);
                        }

                        this.tableData.push(this.temp);
                        this.times++;
                        
                        // 清空输入框
                        this.input = "";

                        // 猜测结束
                        if(this.temp.answer=='True'||this.times==this.settings.maxguess){
                            this.gameover=true
                            this.ReplayAnswer()
                        }
                    }
                }catch(error){
                    console.error(error)
                }
            },
            ValueText(key,value){
                if(value=='high')
                    return String(key)+"↑"
                if(value=='low')
                    return String(key)+"↓"
                return String(key)
            },
            async ReplayAnswer(){
                const answer=sessionStorage.getItem('answer')
                if(answer==null)return;
                try{
                    const options = {
                        method: 'GET',
                        url: `${process.env.VUE_APP_API_BASE_URL}/getanswer`,
                        params:{
                            pokemon:answer
                        } 
                    };
                    await axios.request(options).then((response)=>{
                        this.tempdata=response.data
                    }).catch(function (error) {
                        console.error(error);
                    });
                    const data=this.tempdata
                    console.log(data)

                    try{
                        const options = {
                            method: 'GET',
                            url: `${process.env.VUE_APP_API_BASE_URL}/getimage`,
                            params: {pokemon: data.name},
                            responseType:'blob'
                        };
                        await axios.request(options).then((response)=>{
                            this.tempdata=response.data
                        }).catch(function (error) {
                            console.error(error);
                        });
                        const blob=new Blob([this.tempdata]);
                        this.temp.imgUrl=URL.createObjectURL(blob);
                    }catch(error){
                        console.error('图片获取失败:',error);
                    }

                    this.reply.type=""
                    data.type.forEach((tmp,index)=>{
                        if(index!=0)this.reply.type+="+";
                        this.reply.type+=tmp.key;
                    })
                    
                    this.reply.ability=""
                    data.ability.forEach((tmp,index)=>{
                        if(index!=0)this.reply.ability+=",";
                        this.reply.ability+=tmp.key;
                    })
                    
                    this.reply.label=""
                    data.label.forEach((tmp,index)=>{
                        if(index!=0)this.reply.label+=",";
                        this.reply.label+=tmp.key;
                    })
                    if(this.reply.label=="")
                        this.reply.label="无"

                    const h = this.$createElement;
                    
                    // 修复结果弹窗显示
                    MessageBox({
                        title: '游戏结束',
                        message: h('div', { class: 'result-container' }, [
                            h('div', { class: 'result-image' }, [
                                h('img', {
                                    attrs: {
                                        src: this.temp.imgUrl,
                                        style: 'width: 100px; height: 100px;'
                                    }
                                })
                            ]),
                            h('div', { class: 'result-info' }, [
                                h('p', { class: 'result-name' }, "宝可梦: " + data.name),
                                h('p', { class: 'result-detail' }, "属性: " + this.reply.type),
                                h('p', { class: 'result-detail' }, "种族值: " + data.pow.key),
                                h('p', { class: 'result-detail' }, "特性: " + this.reply.ability),
                                h('p', { class: 'result-detail' }, "其他标签: " + this.reply.label)
                            ])
                        ]),
                        confirmButtonText: '下一把',
                        width: this.isMobile ? '90%' : '50%'
                    }).then(()=>{
                        // 可以在这里添加下一步操作
                    }).catch(()=>{
                        // 处理取消操作
                    });
                }catch(error){
                    console.error(error)
                }
            },
            CloseSetting(){
                this.saveSettings();
                this.settingVisble=false;
                this.Restart();
            },
            ReloadGuessNumber(newvalue){
                if(this.settings.autodif==false)return true;
                this.settings.maxguess=10;
                var x=this.settings.battleOpen*2+this.settings.shapeOpen*2+this.settings.catchOpen;
                if(this.settings.genid!="全世代")this.settings.maxguess-=3,x+=(x<=3);
                if(x==1&&this.settings.catchOpen)x++;
                if(x==2&&this.settings.battleOpen)x++;
                else if(x>=3)x++;
                if(x>=6)this.settings.maxguess-=1;
                if(x>=5)this.settings.maxguess-=1;
                if(x>=4)this.settings.maxguess-=1;
                if(x>=3)this.settings.maxguess-=1;
                if(x>=2)this.settings.maxguess-=1;
                return true;
            },
            saveSettings(){
                console.log("保存设置中")
                try{
                    localStorage.setItem('guessSettings',JSON.stringify(this.settings));
                }catch(e){
                    console.error("设置保存失败：",e);
                }
            },
            loadSettings(){
                try{
                    const savedSettings=localStorage.getItem("guessSettings");
                    if(savedSettings){
                        this.settings=JSON.parse(savedSettings);
                    }
                }catch(e){
                    console.error("设置加载失败：",e);
                }
            },
            handleResize() {
                this.windowWidth = window.innerWidth;
                this.isMobile = window.innerWidth <= 768;
            }
        },
        computed:{
        },
        mounted() {
            this.loadSettings();
            this.Restart();
            window.addEventListener('resize', this.handleResize);
        },
        beforeDestroy() {
            window.removeEventListener('resize', this.handleResize);
        }
    }
</script>

<style>
    .guess {
        margin-top: 20px;
        margin-left: 5%;
        margin-right: 5%;
    }
    
    .times {
        font-size: 1.2rem;
        margin: 20px 0;
        text-align: center;
    }
    
    .setting {
        margin-left: 5%;
        margin-right: 5%;
        display: flex;
        flex-direction: column;
        gap: 12px;
    }
    
    /* 输入区域居中优化 */
    .input-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        max-width: 1200px;
        margin: 0 auto 20px;
    }
    
    .input-row, .button-row {
        width: 100%;
        margin-bottom: 10px;
    }
    
    .button-row {
        margin-top: 10px;
    }
    
    /* 卡片基础样式 */
    .pokemon-cards {
        display: flex;
        margin-bottom: 30px;
    }
    
    .pokemon-card {
        border: 1px solid #EBEEF5;
        border-radius: 8px;
        box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
        background-color: #fff;
        transition: all 0.3s ease;
    }
    
    .pokemon-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 4px 16px 0 rgba(0, 0, 0, 0.15);
    }
    
    .card-header {
        display: flex;
        align-items: center;
        border-bottom: 1px solid #EBEEF5;
    }
    
    .pokemon-image {
        margin-right: 15px;
    }
    
    .pokemon-name {
        font-weight: bold;
    }
    
    .section-title {
        color: #606266;
        font-weight: 500;
    }
    
    .section-content {
        display: flex;
        flex-wrap: wrap;
        gap: 5px;
    }
    
    .info-tag {
        margin: 2px;
    }
    
    /* 移动端卡片样式 */
    .mobile-cards {
        flex-direction: column;
        gap: 15px;
    }
    
    .mobile-cards .pokemon-card {
        padding: 12px;
    }
    
    .mobile-cards .card-header {
        padding-bottom: 10px;
        margin-bottom: 10px;
    }
    
    .mobile-cards .pokemon-name {
        font-size: 16px;
    }
    
    .mobile-cards .card-section {
        margin-bottom: 8px;
        padding-bottom: 8px;
        border-bottom: 1px dashed #EBEEF5;
    }
    
    .mobile-cards .card-section:last-child {
        border-bottom: none;
        margin-bottom: 0;
        padding-bottom: 0;
    }
    
    .mobile-cards .section-title {
        font-size: 14px;
        margin-bottom: 5px;
    }
    
    /* 桌面端卡片样式 - 水平布局 */
    .desktop-cards {
        flex-direction: column;
        gap: 20px;
        margin: 0 auto;
    }
    
    .desktop-card {
        display: flex;
        padding: 0;
        width: 100%;
    }
    
    .desktop-card .card-header {
        flex-direction: column;
        padding: 15px;
        border-bottom: none;
        border-right: 1px solid #EBEEF5;
        align-items: center;
        justify-content: center;
        min-width: 100px;
    }
    
    .desktop-card .pokemon-image {
        margin-right: 0;
        margin-bottom: 10px;
    }
    
    .desktop-card .pokemon-name {
        font-size: 16px;
        text-align: center;
    }
    
    .desktop-card-content {
        display: flex;
        flex: 1;
        padding: 15px;
        overflow-x: auto;
        scrollbar-width: thin;
    }
    
    .desktop-section {
        margin: 0 15px;
        min-width: 100px;
        text-align: center;
    }
    
    .desktop-section .section-title {
        font-size: 14px;
        margin-bottom: 10px;
        border-bottom: 1px dashed #EBEEF5;
        padding-bottom: 5px;
    }
    
    .desktop-section .section-content {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 8px;
    }
    
    /* 修复滚动条样式 */
    .desktop-card-content::-webkit-scrollbar {
        height: 6px;
    }
    
    .desktop-card-content::-webkit-scrollbar-thumb {
        background-color: #c0c4cc;
        border-radius: 3px;
    }
    
    .desktop-card-content::-webkit-scrollbar-track {
        background-color: #f5f7fa;
    }
    
    /* 按钮样式优化 */
    .button-col {
        display: flex;
        justify-content: center;
    }
    
    .action-button {
        width: 100%;
        height: 40px;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    
    /* 按钮文字居中修复 */
    .el-button {
        display: flex;
        justify-content: center;
        align-items: center;
    }
    
    .el-button span {
        display: inline-flex;
        align-items: center;
        justify-content: center;
    }
    
    /* 结果对话框样式 */
    .result-container {
        display: flex;
        align-items: center;
        padding: 15px;
    }
    
    .result-image {
        margin-right: 20px;
    }
    
    .result-info {
        flex: 1;
    }
    
    .result-name {
        font-size: 18px;
        font-weight: bold;
        margin-bottom: 12px;
    }
    
    .result-detail {
        font-size: 15px;
        margin: 8px 0;
    }
    
    /* 响应式调整 */
    @media screen and (max-width: 768px) {
        .guess {
            margin-left: 2%;
            margin-right: 2%;
        }
        
        .times {
            font-size: 1rem;
        }
        
        .result-container {
            flex-direction: column;
            text-align: center;
        }
        
        .result-image {
            margin-right: 0;
            margin-bottom: 15px;
        }
    }
    
    /* 优化头部按钮 */
    .header-buttons {
        display: flex;
        justify-content: flex-end;
        margin-bottom: 10px;
    }
    
    .header-buttons .el-button {
        margin-left: 10px;
    }
</style>
