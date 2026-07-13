from app.Tools.tool import Tool


class CalculatorTool(Tool):
    name = "calculator"

    description = "Perform mathematical calculations."

    def execute(self, **kwargs):

        expression = kwargs.get("expression")

        if not expression:
            raise ValueError("Expression is required.")

        return eval(expression)
