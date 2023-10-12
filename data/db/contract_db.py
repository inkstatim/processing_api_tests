class ContractDb:
    CONTRACT = lambda created_at, year, company_id: {
        "number": "3589856888922885",  # hardcode
        "description": "Voluptas voluptatum id molestiae iste sint.",
        "type": "processing",
        "created_at": created_at,
        "signed_at": created_at,
        "ends_at": f"{year}-01-01 00:00:00.000000",
        "company_id": company_id,
        "number_crc32": 1819463150,
        "terminated_at": 'null'
    }
