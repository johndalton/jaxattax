class FancyForm {
	constructor(element) {
		this._element = element;
	}

	setErrors(errors) {
		self.clearErrors();
		for (field of errors) {
			for (error of errors[field]) {
				this.addFieldError(field, error);
			}
		}
	}

	clearErrors() {
	}

	addFormError(error) {
		console.log("Form error:", error);
	}

	addFieldError(field, error) {
	}
}

export default FancyForm;
