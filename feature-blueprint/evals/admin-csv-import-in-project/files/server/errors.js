export class AppError extends Error {
  constructor(code, userMessage, nextStep, { status = 400, cause } = {}) {
    super(userMessage, { cause });
    this.code = code;
    this.userMessage = userMessage;
    this.nextStep = nextStep;
    this.status = status;
  }
}
