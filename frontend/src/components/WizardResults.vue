<template>
  <div class="main">
    <h2>Results</h2>
    <p>
      You should select a Comma-separated values (CSV) file, where the first row is expected to contain the variable names (column headers). In this version, variables with string values will not be available for calculation.
    </p>
    <p>      
      <!-- accept, extensions, TEST timeout -->
      <file-upload
        ref="upload"
        
        v-model="files"
        post-action="http://127.0.0.1/post"
        
        accept="text/csv"
        :extensions="['csv']"
        :drop="true"
        @input-file="inputFile"
      >
      Upload file
      </file-upload>
      <div v-for="(file, index) in files" :key="index" >
          <progress :value="file.progress"></progress>
      </div>
      <button v-show="!$refs.upload || !$refs.upload.active" @click.prevent="$refs.upload.active = true" type="button">Start upload</button>
      <!--
      <span v-show="$refs.upload && $refs.upload.uploaded">
        All files have been uploaded
      </span>
      -->

      <p>
        <router-link :to="{ name: 'load-database' }" class="start-button">
          Load your database
        </router-link>
      </p>
  </div>
</template>

<script>
import FileUpload from 'vue-upload-component'

export default {
  components: { FileUpload },
  name: 'LoadDatabase',
  data () {
    return {
      files: []
    }
  },
  methods: {
    inputFile: function (newFile, oldFile, prevent) {
      /* if (newFile && !oldFile) {
        if (!/\.(csv)$/i.test(newFile.name)) {
          return prevent()
        }
      }

      if (newFile && oldFile) {
        // Update file

        // Start upload
        if (newFile.active !== oldFile.active) {
          console.log('Start upload', newFile.active, newFile)

          // min size
          if (newFile.size >= 0 && newFile.size < 100 * 1024) {
            newFile = this.$refs.upload.update(newFile, {error: 'size'})
          }
        }

        // Upload progress
        if (newFile.progress !== oldFile.progress) {
          console.log('progress', newFile.progress)
        }

        // Upload error
        if (newFile.error !== oldFile.error) {
          console.log('error', newFile.error)
        }

        // Uploaded successfully
        if (newFile.success !== oldFile.success) {
          console.log('success', newFile.success)
        }
      } */

      newFile.blob = ''
      let URL = window.URL || window.webkitURL
      if (URL && URL.createObjectURL) {
        newFile.blob = URL.createObjectURL(newFile.file)
      }
    }
  }
}
</script>

<style>
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
