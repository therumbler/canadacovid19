"""gather data from each province"""
import asyncio
import logging
import sys
from canadacovid19 import quebec, ontario, canada


logger = logging.getLogger(__name__)


def setup_logging(level):
    logging.basicConfig(stream=sys.stderr, level=level)


async def main():
    coros = [
        quebec.get_data(),
        # ontario.get_data(),
        canada.get_data(),
    ]
    responses = await asyncio.gather(*coros)
    logger.info(responses)


if __name__ == "__main__":
    setup_logging(level=logging.DEBUG)
    asyncio.run(main())
