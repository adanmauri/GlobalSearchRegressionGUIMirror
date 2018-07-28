<template>
  <div>
    <h2>Load your database</h2>
      <p>You should select a Comma-separated values (CSV) file, where the first row is expected to contain the variable names (column headers). In this version, variables with string values will not be available for calculation.</p>
      <div>
        <file-upload
          ref="upload"
          class="file-upload"
          v-model="files"
          :custom-action="customAction"

          :headers="{'X-User-Token': userToken  }"
          accept="text/csv"
          :extensions="['csv']"
          :drop="true"
        >
          <div>
            <div v-for="(file, index) in files" :key="index" class="file-upload-name">
              <span><font-awesome-icon icon="file" class="file-icon" /></span> <span>{{ file.name }}</span>
            </div>
            <p v-if="!files.length">
              <b>Click</b> or <b>drag and drop</b> a CSV file here
            </p>
          </div>
        </file-upload>

        <div v-for="(file, index) in files" :key="index">
          <div class="progress file-upload-progress">
            <div class="progress-bar file-upload-progress-bar" role="progressbar" :style="{ width: file.progress+'%' }" :aria-valuenow="file.progress" aria-valuemin="0" aria-valuemax="100"></div>
          </div>
          <div class="file-upload-progress-speed" >{{ file.speed | speed }}</div>
        </div>
      </div>
      <div class="upload-button-container" v-if="files.length">
        <md-button class="md-icon-button md-raised upload-button"  v-show="!$refs.upload || !$refs.upload.active" @click.prevent="$refs.upload.active = true">
          <font-awesome-icon icon="upload" />
        </md-button>
        <span class="upload-button-label">Start upload</span>
      </div>
        <!--
      <span v-show="$refs.upload && $refs.upload.uploaded">
        All files have been uploaded
      </span>
      -->
  </div>
</template>

<script>
import FileUpload from 'vue-upload-component'
import {mapState} from 'vuex'

export default {
  components: { FileUpload },
  name: 'LoadDatabase',
  filters: {
    speed (value) {
      if (value / 1024 < 1024) {
        return (value / 1024) + ' KB/s'
      }
      return (value / 1024 / 1024).toFixed(2) + ' MB/s'
    }
  },
  data () {
    return {
      files: []
    }
  },
  computed: {
    ...mapState(['userToken'])
  },
  methods: {
    customAction (file) {
      var xhr = new XMLHttpRequest()
      xhr.open('POST', 'http://127.0.0.1:80/post', true)
      xhr.setRequestHeader('X-User-Token', this.$store.state.userToken)
      return new Promise((resolve, reject) => {
        xhr.onload = () => {
          if (xhr.status >= 200 && xhr.status < 300) {
            var response
            try {
              response = JSON.parse(xhr.response)
            } catch (err) {
              response = xhr.response
            }
            resolve(response)
          } else {
            reject(xhr.response)
          }
        }
        xhr.onerror = () => reject(xhr.response)
        xhr.send(file.file)
      })
    },
    inputFilter (newFile, oldFile, prevent) {
      console.log(newFile)
      console.log(oldFile)
      if (newFile && oldFile && newFile.active && !oldFile.active && newFile.file && !newFile.encrypt && /\.pdf$/i.test(newFile.name)) {
        // Has been encrypted
        newFile.encrypt = true
        // Can not use async
        // Do not support IE9
        // https://developer.mozilla.org/en-US/docs/Web/API/File
        // https://developer.mozilla.org/en-US/docs/Web/API/Blob
        // Modify the newFile.file object
        // console.log(newFile.file)
        newFile.file = new File(['xxx'], newFile.name, {type: newFile.type})
      }
    }
  }
}
</script>

<style>
.file-upload {
  width: 100%;
  height: 200px;
  border: 2px dashed #ccc;
  transition: 0.3s border-color;
  cursor: pointer;
}

.file-upload:hover {
  border-color: #60ad51;
}

.file-upload > div {
  display: flex;
  align-items: center;
  height: 90%;
  text-align: center;
}

.file-upload .file-upload-name {
  text-align: center;
  width: 100%;
}

.file-upload .file-upload-name .file-icon {
  font-size: 50px;
  margin-right: 20px;
}

.file-upload-progress {
  margin-bottom: 2px;
  height: 8px;
}

.file-upload-progress-bar {
  background: #60ad51;
}

.file-upload-progress-speed {
  margin-bottom: 2px;
  text-align: right;
  font-size: 15px;
  color: #999;
}

.upload-button-container {
  text-align:right;
  position: relative;
  top: -113px;
  height: 56px;
}

.upload-button:hover + .upload-button-label {
  opacity: 1;
}

.upload-button-label {
  background: rgba(50,50,50,0.8);
  color: #FFF;
  padding: 3px 6px;
  border-radius: 2px;
  font-size: 13px;
  font-weight: bold;
  position: relative;
  top: 15px;
  opacity: 0;
  transition: 0.3s all;
  user-select: none;
}

.upload-button {
  background: #60ad51;
  color: #FFF;
  width: 56px;
  height: 56px;
  text-align: center;
  font-size: 24px;
  outline: none;
  float: right;
}

.upload-button .md-ripple {
  margin-top: -7px;
}

h1 {
  font-weight: normal;
  font-family: "Lato Regular";
  margin-bottom: 0;
}

p {
  max-width: 800px;
  margin: 10px auto;
}

a.start-button {
  text-decoration: none;
  color: #4D63D4;
  font-size: 20px;
  font-family: "Lato Black";
}

.example-drag .drop-active {
    top: 0;
    bottom: 0;
    right: 0;
    left: 0;
    position: fixed;
    z-index: 9999;
    opacity: .6;
    text-align: center;
    background: #000;
  }
  .example-drag .drop-active h3 {
    margin: -.5em 0 0;
    position: absolute;
    top: 50%;
    left: 0;
    right: 0;
    -webkit-transform: translateY(-50%);
    -ms-transform: translateY(-50%);
    transform: translateY(-50%);
    font-size: 40px;
    color: #fff;
    padding: 0;
  }
</style>
