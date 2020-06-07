"""gather data from each province"""
import asyncio
import logging
import sys
from canadacovid19 import quebec, ontario


logger = logging.getLogger(__name__)


def setup_logging(level):
    logging.basicConfig(stream=sys.stderr, level=level)


async def main():
    responses = await asyncio.gather(quebec.get_data(), ontario.get_data())
    logger.info(responses)


if __name__ == "__main__":
    setup_logging(level=logging.DEBUG)
    asyncio.run(main())
