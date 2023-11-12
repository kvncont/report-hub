"""Main file of the application"""

import logging
from typing import Any

import httpx
import jinja2
from fastapi import Depends, FastAPI, HTTPException, Request, Response
from jinja2 import Environment
from weasyprint import HTML

from app.models.report import Report

app = FastAPI()

logger = logging.getLogger(__name__)


async def get_template(request: Request) -> str:
    """
    Get the template from the web server

    Parameters:
        request (Request): The request object

    Returns:
        html_template (str): The html template
    """

    response = None

    body = await request.json()

    async with httpx.AsyncClient() as client:
        try:
            # Send a GET request to the external service where the templates are located
            response = await client.get(body["templateUrl"])

            # Check if the request was successful
            if response.status_code == 404:
                raise HTTPException(status_code=404, detail="Template not found")
        except httpx.ConnectError as exc:
            raise HTTPException(
                status_code=502, detail="Could not connect to the external service"
            ) from exc

    html_template = response.text

    return html_template


def format_number(value):
    """Applies thousand separator to a number, with two decimal places"""
    return "{:,.2f}".format(float(value))


def render_template(template: str, data: dict) -> str:
    """
    Render the html template with the data

    Parameters:
        template (str): The html template
        data (dict): The data to render the template

    Returns:
        rendered_template (str): The rendered html template
    """
    try:
        # Render the template
        env = Environment()
        env.filters["format_number"] = format_number
        template = env.from_string(template)
        # if data is None:
        #     data = {}
        rendered_template = template.render(data)
    except jinja2.exceptions.TemplateSyntaxError as exc:
        logger.exception("Template syntax error")
        raise HTTPException(
            status_code=422,
            detail="Template syntax error",
        ) from exc
    except ValueError as exc:
        logger.exception("Unsupported format character")
        raise HTTPException(
            status_code=422,
            detail="Template syntax error",
        ) from exc

    return rendered_template


@app.post("/v1/report")
async def create_report(
    body: Report, html_template: str = Depends(get_template)
) -> Any:
    """
    Create the pdf report from the template

    Parameters:
        body (Report): The body of the request

    Returns:
        pdf (bytes): PDF report
    """

    logger.info(
        f"Creating PDF report: {body.name}, template template URL: {body.template_url}"
    )

    # Get the template from the web server
    # html_template = await get_template(body.templateUrl)

    # Render the template
    rendered_template = render_template(html_template, body.data)

    # Create html object from rendered content
    html = HTML(string=rendered_template, base_url=body.template_url)

    # Create the PDF
    pdf = html.write_pdf()

    return Response(status_code=200, content=pdf, media_type="application/pdf")
