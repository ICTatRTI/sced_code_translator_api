var watchExampleVM = new Vue({
    el: '#app',
    data: {
      scedCode: null,
      translatedCodes: 'Awaiting input...'
    },
    created: function () {
      document.addEventListener('DOMContentLoaded', function() {
        M.FormSelect.init(document.querySelectorAll('select'));
      })
    },
    watch: {
      scedCode: function () {
        this.translatedCodes = 'Waiting for you to stop typing...',
        this.getTranslations()
      },
    },
    methods: {
      getTranslations: _.debounce(function () {
        if (!this.scedCode) {
          this.translatedCodes = 'Awaiting input...'
          return
        }

        var vm = this
        axios.post('/sced-v7-translate/', {
          sced_code: this.scedCode
        })
          .then(function (response) {
            vm.translatedCodes = response.data.translated_codes;
          })
          .catch(function (error) {
            vm.translatedCodes = 'Error! Could not reach the API. ' + error.msg
          })
        }, 1000) // This is the number of milliseconds we wait for the user to stop typing.
    }
  })
