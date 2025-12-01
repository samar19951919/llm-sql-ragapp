#importing all the required all the required coponents

from typing import List,Tuple,Dict,Any
from sqlalchemy.orm import Session
from sqlalchemy import  text

# importing the ddb from th elocal file 

from app.db.vectorstore import get_vectorstore

# now here we are creatinag a functio to fetch th required views

def fetch_view_rows(db:Session , view_name:str) -> Tuple[List[tuple],List[str]]:

    """here we are trying to emcompasss 
    all the code to fetch the viwes
    
    It returns:
    list off rows as tuples:
    name of colum
    """

    result = db.execute(text(
        f"SELECT * FROM {view_name}"
    ))

    #we can get the rows by using the fetch all with the

    rows = result.fetchall()

    # now for retrieving the columns

    cols = list(result.keys())

    return rows,cols



#=======================CUSTOMER INGESTION=======================

def build_customer_docs(db:Session) -> Tuple[List[str],List[Dict[str,Any]]]:
    '''
    build text + meta data for the customer docs.
    so that ywe can conevrt the whole thin gin to the text.
    '''

    #now fetching the folloowing views 

    rows,cols = fetch_view_rows(db,"customer_profile_docs")

    # now defig the variable for text and meta data

    texts:List[str] = []
    metadatas : List[Dict[str,Any]] = []

    for row in rows:
        rec = dict(zip(cols,row))

        # rec keys from view:
        # doc_id, customer_id, first_name, last_name, email,
        # store_id, active, create_date, last_update,
        # address, address2, district, postal_code, phone,
        # city, country,
        # total_rentals, total_payments, total_spent,
        # first_rental_date, last_rental_date

        full_name = f"{rec['first_name']} {rec['last_name']}"
        address_parts = [
            rec["address"],
            rec.get("address2"),
            rec["district"],
            rec["city"],
            rec["country"],
        ]
        address_str = ", ".join([p for p in address_parts if p])

        text = (
            f"Customer profile for {full_name} "
            f"(customer_id={rec['customer_id']}, email={rec['email']}). "
            f"They are associated with store {rec['store_id']} and live at {address_str}. "
            f"Their phone number is {rec['phone'] or 'N/A'}. "
            f"They have made {rec['total_rentals']} rentals and {rec['total_payments']} payments, "
            f"spending a total of ${rec['total_spent']:.2f}. "
            f"Their first rental was on {rec['first_rental_date']} and the most recent on {rec['last_rental_date']}. "
            f"Account active flag is {rec['active']} (created at {rec['create_date']})."
        )

        texts.append(text)
        metadatas.append(
            {
                "doc_id": str(rec["doc_id"]),
                "entity_type": "customer_profile",
                "customer_id": rec["customer_id"],
                "store_id": rec["store_id"],
                "country": rec["country"],
                "email": rec["email"],
            }
        )

    return texts, metadatas


def ingest_customers(db: Session) -> int:
    """
    Ingest customer profile docs into pgvector.

    Returns number of inserted vectors.
    """
    print("Fetching customer_profile_docs_with_id...")
    texts, metadatas = build_customer_docs(db)
    print(f"Found {len(texts)} customer docs. Inserting into vector store...")

    if not texts:
        print("No customer docs to ingest.")
        return 0

    vs = get_vectorstore()
    ids = vs.add_texts(texts=texts, metadatas=metadatas)
    print(f"Ingested {len(ids)} customer profile vectors.")
    return len(ids)


# ==========
# FILM INGESTION
# ==========

def build_film_docs(db: Session) -> Tuple[List[str], List[Dict[str, Any]]]:
    """
    Build text + metadata for film profiles from:
      view: film_profile_docs_with_id
    """
    rows, cols = fetch_view_rows(db, "film_profile_docs")

    texts: List[str] = []
    metadatas: List[Dict[str, Any]] = []

    for row in rows:
        rec = dict(zip(cols, row))

        # rec keys from view:
        # doc_id, film_id, title, description, release_year,
        # language_id, original_language_id, rental_duration,
        # rental_rate, length, replacement_cost,
        # rating, last_update, special_features, actors

        actors = rec["actors"] or "Unknown cast"
        description = rec["description"] or "No description available"

        text = (
            f"Film profile: {rec['title']} (film_id={rec['film_id']}). "
            f"Description: {description} "
            f"Release year: {rec['release_year']}. "
            f"Rating: {rec['rating'] or 'Unrated'}. "
            f"Rental rate is {rec['rental_rate']} for a duration of {rec['rental_duration']} days. "
            f"Length: {rec['length']} minutes. Replacement cost: {rec['replacement_cost']}. "
            f"Special features: {rec['special_features'] or 'None listed'}. "
            f"Actors in this film: {actors}."
        )

        texts.append(text)
        metadatas.append(
            {
                "doc_id": str(rec["doc_id"]),
                "entity_type": "film_profile",
                "film_id": rec["film_id"],
                "title": rec["title"],
                "rating": rec["rating"],
                "release_year": rec["release_year"],
            }
        )

    return texts, metadatas


def ingest_films(db: Session) -> int:
    """
    Ingest film profile docs into pgvector.

    Returns number of inserted vectors.
    """
    print("Fetching film_profile_docs_with_id...")
    texts, metadatas = build_film_docs(db)
    print(f"Found {len(texts)} film docs. Inserting into vector store...")

    if not texts:
        print("No film docs to ingest.")
        return 0

    vs = get_vectorstore()
    ids = vs.add_texts(texts=texts, metadatas=metadatas)
    print(f"Ingested {len(ids)} film profile vectors.")
    return len(ids)


# ==========
# ACTOR INGESTION
# ==========

def build_actor_docs(db: Session) -> Tuple[List[str], List[Dict[str, Any]]]:
    """
    Build text + metadata for actor profiles from:
      view: actor_profile_docs_with_id
    """
    rows, cols = fetch_view_rows(db, "actor_profile_docs")

    texts: List[str] = []
    metadatas: List[Dict[str, Any]] = []

    for row in rows:
        rec = dict(zip(cols, row))

        # rec keys from view:
        # doc_id, actor_id, first_name, last_name,
        # last_update, film_count, films

        full_name = f"{rec['first_name']} {rec['last_name']}"
        films = rec["films"] or "No films listed"

        text = (
            f"Actor profile: {full_name} (actor_id={rec['actor_id']}). "
            f"They appear in {rec['film_count']} films. "
            f"Filmography: {films}. "
            f"Record last updated at {rec['last_update']}."
        )

        texts.append(text)
        metadatas.append(
            {
                "doc_id": str(rec["doc_id"]),
                "entity_type": "actor_profile",
                "actor_id": rec["actor_id"],
                "actor_name": full_name,
                "film_count": rec["film_count"],
            }
        )

    return texts, metadatas


def ingest_actors(db: Session) -> int:
    """
    Ingest actor profile docs into pgvector.

    Returns number of inserted vectors.
    """
    print("Fetching actor_profile_docs_with_id...")
    texts, metadatas = build_actor_docs(db)
    print(f"Found {len(texts)} actor docs. Inserting into vector store...")

    if not texts:
        print("No actor docs to ingest.")
        return 0

    vs = get_vectorstore()
    ids = vs.add_texts(texts=texts, metadatas=metadatas)
    print(f"Ingested {len(ids)} actor profile vectors.")
    return len(ids)


# ==========
# INGEST ALL
# ==========

def ingest_all_profiles(db: Session) -> Dict[str, int]:
    """
    Convenience helper to ingest customers, films, and actors in one go.
    Returns counts per entity type.
    """
    c = ingest_customers(db)
    f = ingest_films(db)
    a = ingest_actors(db)

    return {
        "customers_indexed": c,
        "films_indexed": f,
        "actors_indexed": a,
    }





     












