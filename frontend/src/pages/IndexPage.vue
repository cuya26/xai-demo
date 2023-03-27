<template>
  <q-page padding class="row items-strech">
    <div class="col-12 column no-wrap">
      <div class="row no-wrap justify-between" style="height: 100%">
        <div class="column no-wrap" style="width: 55%">
          <div class="q-pb-md">
            <div style="height:40px"></div>
          </div>
          <q-card
            class="items-strech"
            style="height: 680px"
          >
            <div
              class="col-12 column no-wrap"
              style="height: 100%"
            >
              <q-card-section class="row justify-between">
                <div class="col-3"></div>
                <div class="text-h6 text-primary">Input</div>
                <div class="col-3">
                  <div class="col-6 justify-end row">
                    <q-btn v-if="inputMode==='saliency'" label="text" color="primary" flat rounded dense @click="inputMode='edit'" />
                  </div>
                  <!-- <div class="col-6 justify-end row">
                    <q-btn v-if="inputMode!=='pdf' && dropzoneURL!==''" label="pdf" class="text-primary" flat rounded dense @click="inputMode='pdf'" />
                  </div> -->
                  <q-btn-toggle
                    v-model="inputMode"
                    style="border: 1px solid #027be3"
                    no-caps
                    dense
                    spread
                    v-if='dropzoneURL!=="" && inputMode!=="saliency"'
                    rounded
                    unelevated
                    toggle-color="primary"
                    color="white"
                    text-color="primary"
                    :options="[
                      {label: 'PDF', value: 'pdf'},
                      {label: 'TEXT', value: 'edit'}
                    ]"
                  />
                </div>
              </q-card-section>
              <q-card-section style="height: 90%">
                <div
                  v-if="!loadingSaliencyMap"
                  style="overflow: auto; flex-grow: 1;max-height: 100%"
                >
                  <q-input
                  @drop.prevent="this.dropFunction"
                  @dragover.prevent
                  @dragenter.prevent="highlightColor = true"
                  @dragleave="highlightColor = false"
                  :class="
                    (highlightColor ? 'bg-light-blue-2' : '') +
                    ' text-grey-7'
                  "
                  v-if="inputMode==='edit'"
                  outlined
                  placeholder="Insert text or drag and drop a pdf of txt file"
                  class="text-grey-7"
                  type="textarea"
                  input-style="min-height: 560px;white-space: nowrap;overflow-x: scroll;font-family: monospace;font-size: small"
                  style=""
                  v-model="inputLetter"
                  />
                  <embed
                    :src="dropzoneURL"
                    style="min-height: 560px;width: 100%"
                    class=""
                    v-if="inputMode==='pdf'"
                    type="application/pdf"
                  />
                  <!-- <q-input outlined v-model="text" :dense="dense" /> -->
                  <!-- <div class="text-grey-7" style="white-space: pre-line">{{dischargeLetterName == null ? '' : letterDict[dischargeLetterName]}}</div> -->
                </div>

                <div style="height: 100%;" v-if="loadingSaliencyMap" class="row justify-evenly">
                  <div style="height: 100%;" class="column justify-evenly">
                    <q-spinner color="primary" size="6em" />
                  </div>
                </div>
                <div v-if="inputMode==='saliency'" class="text-grey-7" style="overflow: auto; flex-grow: 1;max-height: 100%">
                  <div style="min-height: 490px; white-space: pre-line">
                  <mark style="white-space: pre-line;" v-for="element in saliencyMap" :key="element" :class="element.color">
                    {{ element.text }}
                  </mark>
                  </div>
                </div>
              </q-card-section>
            </div>
          </q-card>
        </div>

        <div class="column no-wrap" style="width: 42%">

          <!-- <div class="q-pb-md">
            <div class="row justify-evenly">
              <q-select
                outlined
                v-model="taskName"
                :options="taskOptionGroups"
                dense
                label="Choose a Task"
                @update:model-value="updateTaskName"
                style="width: 48%"
              >
                <template v-slot:option="scope">
                  <q-item v-if="!scope.opt.group"
                    v-bind="scope.itemProps"
                  >
                    <q-item-section>
                      <q-item-label class="q-pl-md">{{ scope.opt.label }}</q-item-label>
                    </q-item-section>
                  </q-item>
                  <q-item v-if="scope.opt.group"
                  >
                    <q-item-section>
                      <q-item-label class="text-bold text-primary">{{ scope.opt.group + ':' }}</q-item-label>
                    </q-item-section>
                  </q-item>
                </template>
              </q-select>
              <q-select
              style="width: 48%"
              dense
              outlined
              v-model="setupName"
              :options="taskName?taskOptionGroups.filter(optionTask => optionTask.value === taskName)[0]['modelNames']:[]"
              label="Choose a Model"
              @update:model-value="whenChangeSetupModel"
              />
            </div>
          </div> -->

          <div class="q-pb-md">
            <div style="height:40px"></div>
          </div>

          <!-- Model Output Card -->
          <q-card class="" style="height: 680px">
            <q-card-section class=" row justify-between" >
              <div class="col-2"></div>
              <div class="text-h6 text-primary">Output</div>
              <div class="col-2" v-if="!computed"></div>
                <div v-if="computed" class="col-2 justify-end row">
                  <q-btn label="Reset" class="text-primary" flat rounded dense @click="computed=false" />
                </div>
            </q-card-section>
            <q-card-section
            class="" style="height: 90%"
            >
              <div v-if="!computed" class="q-pt-sm column justify-begin no-wrap" style="height:100%">
                <div class=" q-pb-md row justify-evenly items-center">
                  <q-btn
                  style="width: 100px"
                  dense
                  :disable="inputLetter===null"
                  label="compute"
                  rounded
                  :loading="loading"
                  color="primary"
                  @click="computeOutput()"
                />
                </div>
              </div>
              <div v-show="computed" class="q-pa-md q-m" style="white-space: pre-line; max-height: 560px; min-height: 560px ;overflow:auto; border: 1px solid rgba(0, 0, 0, 0.24);border-radius: 4px;">
                {{ outputText }}
              </div>
            </q-card-section>
          </q-card>
        </div>
      </div>
    </div>
  </q-page>
</template>

<style lang="sass">
.my-sticky-virtscroll-table
  /* height or max-height is important */
  height: 500px

  .q-table__top,
  .q-table__bottom,
  thead tr:first-child th /* bg color is important for th; just specify one */
    background-color: #fff

  thead tr th
    position: sticky
    z-index: 1
  /* this will be the loading indicator */
  thead tr:last-child th
    /* height of all previous header rows */
    top: 48px
  thead tr:first-child th
    top: 0
</style>

<script>
import { defineComponent, ref } from 'vue'
import { api } from 'boot/axios'


export default defineComponent({
  name: 'IndexPage',
  setup () {
    return {
      outputText: ref(""),
      computed: ref(false),
      inputMode: ref("edit"),
      dropzoneURL: ref(""),
      text: ref(""),
      highlightColor: ref(false),
      loadingSaliencyMap: ref(false),
      showSaliencyMap: ref(false),
      saliencyMap: ref([]),
      inputLetter: ref(null),
      taskName: ref(null),
      taskOptionGroups: [
        {
          group: 'Genomic Description',
          disable: true
        },
        {
          label: 'Binding Site Search',
          value: 'binding-site-search',
          modelNames: [
            'flan-t5 finetuned'
          ]
        }
      ],
      upload: ref(null),
      dischargeLetterLoaded: ref(false),
      dischargeLetterName: ref(null),
      letterNames: ref([]),
      letterDict: ref({}),
      setupName: ref(null),
      setupNames: ref({
        "Binding Site Search" : ['flan-t5 finetuned']
      }),
      loading: ref(false),
      modelConfig: ref(
        {
          "flan-t5 finetuned": {
            modelName: "google/flan-t5-small",
            lang: "multi",
            modelType: 't5',
            thresold: 0.6
          }

        }
      )
    }
  },
  methods : {
    loadSaliencyMapQA (sliceIndex, answer, answer_index, question) {
      this.loadingSaliencyMap = true
      api.post(
        '/compute_saliency_map',
        {
          task_type: 'qa',
          input_text: this.inputLetter,
          slice_index: sliceIndex,
          answer: answer,
          question: question,
          model_type: this.modelConfig[this.setupName].modelType,
          model_name: this.modelConfig[this.setupName].modelName,
          model_lang: this.modelConfig[this.setupName].lang,
        },
        { timeout: 360000 }
      ).then ( (response) => {
        this.loadingSaliencyMap = false
        this.inputMode="saliency"
        console.log(response.data.saliency_map)
        console.log(this.freeQuestionResponse)
        this.saliencyMap = response.data.saliency_map
      }).catch( (error) =>{
        this.loadingSaliencyMap = false
        console.log('ops an error occurs during the computing of the saliency maps')
        error.message
      })
    },
    loadSaliencyMapDrugExtraction (sentence, target, colName) {

      this.loadingSaliencyMap = true
      api.post(
        '/compute_saliency_map',
        {
          task_type: 'drug_event_extraction',
          task: colName,
          input_text: this.inputLetter,
          sentence: sentence,
          target_text: target,
          model_type: this.modelConfig[this.setupName][colName].modelType,
          model_name: this.modelConfig[this.setupName][colName].modelName,
          model_lang: this.modelConfig[this.setupName][colName].lang,
        },
        { timeout: 360000 }
      ).then ( (response) => {
        this.loadingSaliencyMap = false
        this.inputMode="saliency"
        this.saliencyMap = response.data.saliency_map
      }).catch( (error) =>{
        this.loadingSaliencyMap = false
        console.log('ops an error occurs during the computing of the saliency maps')
        error.message
      })
    },
    extractValues () {
      this.loading=true
      api.post(
        '/extract_data_table',
        { input_text: this.inputLetter}
      ).then( (response) => {
        this.loading=false
        console.log(response.data)
        this.medicationList = response.data
      }).catch((error)=>{
        this.loading=false
        console.log('ops an error occurs')
        error.message
      })
    },
    answerQuestion () {
      this.loading=true
      this.inputMode="edit"
      this.freeQuestionResponse = {answers: [], noAnswer: false}
      api.post(
        '/answer_question',
        {
          model_type: this.modelConfig[this.setupName].modelType,
          model_name: this.modelConfig[this.setupName].modelName,
          model_lang: this.modelConfig[this.setupName].lang,
          // answer_number: this.modelConfig[this.setupName].answerNumber,
          input_text: this.inputLetter,
          question: this.question,
          compute_saliency_map: false,
        },
        { timeout: 360000 },
      ).then( (response) => {
        this.loading=false
        console.log(response.data)
        this.freeQuestionResponse = response.data
        let noAnswer = true
        for (const answer of this.freeQuestionResponse.answers ){
          if (answer.score.toFixed(3) > this.modelConfig[this.setupName].thresold){
            noAnswer = false
          }
          // if (answer.text !== ''){
          //   noAnswer = false
          // }
        }
        console.log(noAnswer)
        // this.freeQuestionResponse['noAnswer'] = noAnswer
        // if (!noAnswer){
        //   // TODO ordina risposte
        //   this.freeQuestionResponse.answers = this.freeQuestionResponse.answers.slice(0,3)
        // }
      }).catch((error)=>{
        this.loading=false
        console.log('ops an error occurs')
        error.message
      })
    },
    answerQuestionList () {
      this.loading=true
      his.inputMode="edit"
      let modelType = null
      if (this.taskName == "question answering (extractive)") modelType = 'extractive'
      else modelType = 'generative'
      let lang = this.modelConfig[this.setupName].lang
      api.post(
        '/answer_question_list',
        {
          model_type: modelType,
          model_name: this.modelConfig[this.setupName].modelName,
          model_lang: lang,
          input_text: this.inputLetter,
          question_answer_list: this.defaultQuestionsAnswers[lang],
          compute_saliency_map: false
        },
        { timeout: 360000 },
      ).then( (response) => {
        this.loading=false
        console.log(response.data)
        this.defaultQuestionsAnswers[lang] = response.data
      }).catch((error)=>{
        this.loading=false
        console.log('ops an error occurs')
        error.message
      })
    },
    deidentify () {
      this.loading = true

      let deidentificationModelDict = {}
      for ( const [entityType, entityTypeDict] of Object.entries(this.deidentificationConf['custom'])) {
        if ( this.deidentificationConf[this.setupName][entityType] ) {
          deidentificationModelDict[entityType] = this.deidentificationConf[this.setupName][entityType].value
        } else {
          deidentificationModelDict[entityType] = ''
        }
      }
      console.log(deidentificationModelDict)
      api.post(
        '/deidentify',
        {
        cfg: {
          models: deidentificationModelDict,
          mask: {
            mode: "tag",
            special_character: "*",
            date_level: this.dictDateAnonymLevel[this.dateAnonymLevel]
          }
        },
        input_text: this.inputLetter
      }).then( (response) => {
        let deidentifiedText = response.data['deidentified_text']
        this.$refs.deidentifiedTextDiv.innerHTML = this.highlight(deidentifiedText)
        // this.deidentifiedText = this.deidentifiedText.replace(/<DATA>/, '<span class="bg-primary"><DATA></span>')
        this.deidentified = true
        this.loading = false
      }).catch( (error) => {
        this.loading=false
        console.log('ops an error occurs')
        error.message
      })
    },
    highlight (text) {

      text = text.replace(/</g, '&lt').replace(/>/g, '&gt')

      text = text.replace(/&ltTELEFONO&gt/g, '<span class="bg-yellow-3">&ltTELEFONO&gt</span>')
      text = text.replace(/&ltCAP&gt/g, '<span class="bg-brown-3">&ltCAP&gt</span>')
      text = text.replace(/&ltE-MAIL&gt/g, '<span class="bg-indigo-3">&ltE-MAIL&gt</span>')
      text = text.replace(/&ltPERSONA&gt/g, '<span class="bg-pink-3">&ltPERSONA&gt</span>')
      text = text.replace(/&ltORGANIZZAZIONE&gt/g, '<span class="bg-teal-3">&ltORGANIZZAZIONE&gt</span>')
      text = text.replace(/&ltINDIRIZZO&gt/g, '<span class="bg-orange-3">&ltINDIRIZZO&gt</span>')
      text = text.replace(/&ltDATA&gt/g, '<span class="bg-green-3">&ltDATA&gt</span>')
      text = text.replace(/&ltCF&gt/g, '<span class="bg-red-4">&ltCF&gt</span>')
      text = text.replace(/&ltETÀ&gt/g, '<span class="bg-purple-4">&ltETÀ&gt</span>')

      // this.$refs.deidentifiedTextDiv.$el
      // this.$refs.deidentifiedTextDiv.replace(/prova/, '<span>prova</span>')
      // this.$refs.deidentifiedTextDiv.innerHTML = this.$refs.deidentifiedTextDiv.innerHTML.replace(/<DATA>/, '<span>####</span>')
      return text
    },
    loadLetters (upload) {
      var reader = new FileReader()
      reader.onload = (e) => {
        // console.log(reader.result)
        // console.log(e)
        const sessionJSON = JSON.parse(reader.result)
        // console.log(sessionJSON)
        this.letterDict = sessionJSON
        this.letterNames = Object.keys(this.letterDict).sort((a, b) => {
          if (a.split('_')[0].length !== b.split('_')[0].length) return b.split('_')[0].length - a.split('_')[0].length
          else return parseInt(a.split('_')[1]) - parseInt(b.split('_')[1])
        })
        this.dischargeLetterLoaded = true
      }
      reader.readAsText(upload)
    },
    whenChangeSetupModel () {
      // reset answer question ansqwering model
      if ( this.taskName.includes('question') ){
        this.freeQuestionResponse = {answers: [], noAnswer: false}
        for ( const lang of Object.keys(this.defaultQuestionsAnswers) ) {
          for ( const index of Object.keys(this.defaultQuestionsAnswers[lang]) )
            this.defaultQuestionsAnswers[lang][index]["answer"] = null
            this.question = null
        }
      }
      // reset
      this.deidentified = false
    },
    resetDeidModel(value, entityType) {
      if (value === true ) this.deidentificationConf[this.setupName][entityType].value = this.deidentificationConf[this.setupName][entityType].default
      if (value === false) this.deidentificationConf[this.setupName][entityType].value = ''
    },
    updateTaskName () {
      this.setupName = null
      this.taskName = this.taskName.value
    },
    dropFunction(dragEvent) {
      // TODO add revokeObjectURL
      const dropzoneFile = dragEvent.dataTransfer.files[0];
      // TODO add docx
      if (dropzoneFile.type === "application/pdf") {
        this.dropzoneURL = URL.createObjectURL(dropzoneFile);
        this.inputMode = 'pdf'
        // console.log(dropzoneFile);
        // console.log(dragEvent.dataTransfer);
        // console.log(this.dropzoneURL);
        const uploadForm = new FormData();
        uploadForm.append("uploaded_pdf", dropzoneFile);
        // uploadForm.append("notes", "this are my notes");
        api
          .post("convert_pdf", uploadForm, {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          })
          .then((response) => {
            this.inputLetter = response.data["pdf_text"];
          })
          .catch((error) => {
            console.log(error.message);
          });
      } else if (dropzoneFile.type === "text/plain") {
        const reader = new FileReader();
        reader.onload = (res) => {
          this.inputLetter = res.target.result;
        };
        reader.onerror = (err) => console.log(err);
        reader.readAsText(dropzoneFile);
      } else {
        // TODO add error message
        console.log("The dropped file haven't a supported extension");
      }
      this.highlightColor = false;
    },
    computeOutput() {
      // Call backend
      this.loading = true
      api.post(
        '/compute_output',
        {
        input_text: this.inputLetter
      }).then( (response) => {
        this.outputText = response.data['output_text']
        this.computed = true
        this.loading = false
      }).catch( (error) => {
        this.loading=false
        console.log('ops an error occurs calling the model')
        error.message
      })
    }
  },
  created () {

  }
})
</script>
