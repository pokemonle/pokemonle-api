<template>
  <el-dialog
    title="设置"
    :visible.sync="visible"
    :width="isMobile ? '90%' : '50%'"
    :show-close="false"
    :before-close="Close"
    :close-on-click-modal="false"
    :close-on-press-escape="false"
    custom-class="enhanced-dialog"
  >
    <div class="setting">
      <div class="setting-section">
        <div class="setting-title">游戏模式</div>
        <el-select
          v-model="settings.hardid"
          placeholder="请选择"
          size="small"
          style="width: 50%"
        >
          <el-option
            v-for="item in difficulty"
            :key="item"
            :label="item"
            :value="item"
          >
          </el-option>
        </el-select>
      </div>
      <div class="setting-section">
        <div class="setting-title">世代选择 {{ gen }}</div>
        <div class="gen-selection">
          <div class="gen-checkboxes">
            <el-checkbox-group v-model="checkedGens" :min="1">
              <el-checkbox
                v-for="gen in genList"
                :key="gen.id"
                :label="gen.identifier"
                @change="
                  (val) => {
                    handleGenChange(gen.id, val);
                  }
                "
              >
                {{ gen.name }}
              </el-checkbox>
            </el-checkbox-group>
          </div>
        </div>
      </div>

      <div class="setting-section">
        <div class="setting-title">显示信息</div>
        <div class="switch-group">
          <el-switch
            v-model="settings.battleOpen"
            active-text="显示更多种族值信息"
          >
          </el-switch>
          <el-switch
            v-model="settings.shapeOpen"
            active-text="显示更多外形信息"
          >
          </el-switch>
          <el-switch
            v-model="settings.catchOpen"
            active-text="显示蛋组/捕获率信息"
          >
          </el-switch>
        </div>
      </div>

      <el-switch v-model="settings.showGenArrow" active-text="开启世代箭头">
      </el-switch>

      <el-tooltip
        class="item"
        effect="dark"
        content="宝可梦们会随机挡住某个词条"
        placement="top-start"
      >
        <el-switch v-model="settings.cheatOpen" active-text="小小的恶作剧">
        </el-switch>
      </el-tooltip>
      <br />

      <div class="block">
        <span class="demonstration"
          >猜测次数：{{ this.settings.maxguess }}</span
        >
        <el-slider
          v-model="settings.maxguess"
          :step="1"
          :max="15"
          :min="3"
          style="width: 100%"
        >
        </el-slider>
      </div>
    </div>

    <div slot="footer" class="dialog-footer">
      <el-button type="primary" @click="Close">确 定</el-button>
    </div>
  </el-dialog>
</template>

<script>
import { getGen } from "@/api/gen";

export default {
  name: "Setting",
  props: {
    visible: {
      type: Boolean,
      default: false,
    },
    gen: {
      type: Number,
      // default: 0,
    },
  },
  data() {
    return {
      isMobile: window.innerWidth <= 768,
      difficulty: ["普通模式", "简单模式"],
      genList: [],
      checkedGens: [],
      settings: {
        genid: "全世代",
        selectedGens: [true, true, true, true, true, true, true, true, true],
        hardid: "普通模式",
        genid: "全世代", // 保留以兼容旧数据
        selectedGens: [true, true, true, true, true, true, true, true, true], // 默认全选
        maxguess: 10,
        battleOpen: false,
        shapeOpen: false,
        catchOpen: false,
        cheatOpen: false,
        showGenArrow: true,
      },
    };
  },
  methods: {
    Close() {
      this.$emit("update:visible", false);
    },
    handleGenChange(id, check) {
      this.updateGen(this.gen ^ (1 << (id - 1)));
    },

    updateGen(val) {
      this.$emit("update:gen", val);
    },
  },
  mounted() {
    getGen().then((res) => {
      this.genList = res.data;
      this.checkedGens = this.genList.map((gen) => gen.identifier);
      this.updateGen((1 << this.genList.length) - 1);
    });
  },
};
</script>
