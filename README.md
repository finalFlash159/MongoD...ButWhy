### What is MongoDB Atlas?
MongoDB is a document-oriented database. Simply put, you get the scalability and flexibility you want, with the querying and indexing features you need.

```python
# Connect to MongoDB instance running on localhost
client = pymongo.MongoClient()                   

# Access the 'restaurants' collection
# in the 'test' database
collection = client.test.restaurants
```

## MongoDB Database

### Documents

MongoDB stores data records as BSON documents. BSON is a binary representation of JSON documents, though it contains more data types than JSON. For the BSON spec, see bsonspec.org. See also BSON Types.
![](https://www.mongodb.com/docs/manual/images/crud-annotated-document.svg)

### Document Structure
```json
{
   field1: value1,
   field2: value2,
   field3: value3,
   ...
   fieldN: valueN
}
```

The value of a field can be any of the BSON data types, including other documents, arrays, and arrays of documents. For example, the following document contains values of varying types:
```json
var mydoc = {
               _id: ObjectId("5099803df3f4948bd2f98391"),
               name: { first: "Alan", last: "Turing" },
               birth: new Date('Jun 23, 1912'),
               death: new Date('Jun 07, 1954'),
               contribs: [ "Turing machine", "Turing test", "Turingery" ],
               views : NumberLong(1250000)
            }
```

- `_id` holds an **ObjectId.**

- `name` holds an embedded document that contains the fields `first` and `last`.

- `birth` and `death` hold values of the **Date type.**

- `contribs` holds an **array of strings.**

- `views` holds a value of the **NumberLong type.**

## BSON Types trong MongoDB

BSON (Binary JSON) là định dạng tuần tự hoá nhị phân được sử dụng để lưu trữ document và thực hiện remote procedure calls trong MongoDB. Bạn có thể tìm hiểu thêm về định nghĩa BSON tại [bsonspec.org](http://bsonspec.org).

Mỗi BSON type có cả định danh kiểu số (integer) và chuỗi (string) như sau:

| Type                  | Number | Alias      | Notes                                               |
|-----------------------|--------|------------|-----------------------------------------------------|
| Double                | 1      | "double"   |                                                     |
| String                | 2      | "string"   |                                                     |
| Object                | 3      | "object"   |                                                     |
| Array                 | 4      | "array"    |                                                     |
| Binary data           | 5      | "binData"  |                                                     |
| Undefined             | 6      | "undefined"| Deprecated.                                         |
| ObjectId              | 7      | "objectId" |                                                     |
| Boolean               | 8      | "bool"     |                                                     |
| Date                  | 9      | "date"     |                                                     |
| Null                  | 10     | "null"     |                                                     |
| Regular Expression    | 11     | "regex"    |                                                     |
| DBPointer             | 12     | "dbPointer"| Deprecated.                                         |
| JavaScript            | 13     | "javascript"|                                                    |
| Symbol                | 14     | "symbol"   | Deprecated.                                         |
| 32-bit integer        | 16     | "int"      |                                                     |
| Timestamp             | 17     | "timestamp"|                                                     |
| 64-bit integer        | 18     | "long"     |                                                     |
| Decimal128            | 19     | "decimal"  |                                                     |
| Min key               | -1     | "minKey"   |                                                     |
| Max key               | 127    | "maxKey"   |                                                     |

Các toán tử như `$type` (trong query hoặc aggregation) sử dụng các giá trị này để truy vấn các trường theo kiểu BSON của chúng.

---

## Các Loại BSON Đặc Biệt

### 1. Binary Data

- **Giải thích:**  
  BSON binary binData là một mảng byte. Mỗi giá trị binData có một subtype cho biết cách giải thích dữ liệu nhị phân đó.

- **Bảng subtypes của Binary Data:**

  | Number | Description                                  |
  |--------|----------------------------------------------|
  | 0      | Generic binary subtype                       |
  | 1      | Function data                                |
  | 2      | Binary (old)                                 |
  | 3      | UUID (old)                                   |
  | 4      | UUID                                         |
  | 5      | MD5                                          |
  | 6      | Encrypted BSON value                         |
  | 7      | Compressed time series data (New in version 5.2)|
  | 8      | Sensitive data (ví dụ: key, secret). MongoDB không log giá trị thật mà chỉ log placeholder. |
  | 9      | Vector data (dãy số được đóng gói chặt)       |
  | 128    | Custom data                                  |

---

### 2. ObjectId

- **Giải thích:**  
  ObjectId là 12 byte, được thiết kế để tạo ra các giá trị gần như duy nhất, nhanh chóng và có thứ tự tương đối. Cấu trúc của ObjectId gồm:
  - **4 byte**: Timestamp (số giây kể từ Unix epoch).
  - **5 byte**: Giá trị ngẫu nhiên được tạo ra một lần cho mỗi process (đảm bảo tính duy nhất cho máy và process).
  - **3 byte**: Bộ đếm tăng dần, được khởi tạo ngẫu nhiên.

- **Lưu ý:**  
  - Các byte quan trọng nhất (timestamp và counter) được lưu theo thứ tự big-endian, khác với hầu hết các giá trị BSON khác (little-endian).
  - Nếu khởi tạo ObjectId từ một số nguyên, số đó sẽ thay thế timestamp.
  - Mỗi document trong một collection thông thường phải có trường `_id` duy nhất, và nếu thiếu, driver MongoDB sẽ tự động tạo ObjectId.
  - Bạn có thể sử dụng phương thức `ObjectId.getTimestamp()` (trong `mongosh`) để lấy thời gian tạo ObjectId.
  - Mặc dù ObjectIds theo thứ tự xấp xỉ theo thời gian tạo, chúng không đảm bảo thứ tự tuyệt đối vì có độ phân giải chỉ đến giây và do đồng hồ hệ thống có thể không đồng bộ.

---

### 3. String

- **Giải thích:**  
  BSON strings được lưu dưới dạng UTF-8. Điều này có nghĩa là khi chuyển từ string của ngôn ngữ lập trình sang BSON, hầu hết các ký tự quốc tế đều được hỗ trợ.
  - Các truy vấn `$regex` trong MongoDB cũng hỗ trợ chuỗi UTF-8.

---

### 4. Timestamps

- **Giải thích:**  
  BSON có một loại timestamp riêng biệt cho mục đích nội bộ của MongoDB, không liên quan đến kiểu `Date`.  
  - Timestamp BSON là một giá trị 64-bit:
    - **32-bit**: giá trị `time_t` (số giây từ Unix epoch).
    - **32-bit**: số thứ tự tăng dần cho các thao tác trong cùng một giây.
  - Mặc dù BSON là little-endian, `mongod` luôn so sánh phần `time_t` trước khi xét đến số thứ tự, bất kể endianness.
  - Timestamp thường được sử dụng trong replication (ví dụ: trường `ts` trong oplog), và mỗi giá trị trong oplog là duy nhất.

> **Lưu ý:** Thông thường, trong phát triển ứng dụng, bạn sẽ dùng kiểu Date thay vì timestamp BSON.

---

### 5. Date

- **Giải thích:**  
  BSON Date là một số nguyên 64-bit đại diện cho số mili-giây kể từ Unix epoch (1/1/1970).  
  - Cho phép biểu diễn khoảng thời gian rộng, gần 290 triệu năm vào quá khứ và tương lai.
  - BSON Date được coi là UTC datetime.
  - Giá trị Date là số có dấu, nên các giá trị âm biểu diễn thời gian trước năm 1970.
  
**Ví dụ tạo Date trong mongosh:**

```javascript
// Sử dụng new Date()
var mydate1 = new Date();

// Sử dụng ISODate()
var mydate2 = ISODate();
```

#### Field Names
Trong MongoDB, tên field luôn là chuỗi (string) và có một số quy định và giới hạn như sau:

1. **Field `id`:**
   - Field `id` là field đặc biệt dành cho primary key. 
   - Giá trị của `id` phải là duy nhất trong mỗi collection và không được phép thay đổi (immutable).
   - `id` có thể là bất kỳ kiểu dữ liệu nào, ngoại trừ array hoặc regex.
   - Nếu `id` chứa các subfield (trường con), thì tên của các subfield không được bắt đầu bằng ký tự ($).

2. **Giới hạn về ký tự trong tên field:**
   - Tên field không được chứa ký tự null (null character).
   - Mặc dù MongoDB cho phép lưu trữ tên field chứa dấu chấm (`.`) và dấu đô la (`$`), phiên bản MongoDB 5.0 trở đi có hỗ trợ cải tiến cho việc sử dụng (`$`) và (``.``) trong tên field với một số hạn chế nhất định (tham khảo thêm phần Field Name Considerations).

3. **Tính duy nhất của tên field trong một document:**
   - Mỗi tên field trong một document phải là duy nhất. Không được lưu trữ document có tên field trùng lặp.
   - Các thao tác CRUD (create, read, update, delete) của MongoDB có thể hoạt động không như mong muốn nếu document chứa các field trùng lặp.
   - Mặc dù một số thư viện xây dựng BSON có thể cho phép tạo document với các tên field trùng lặp, nhưng việc chèn (insert) những document này vào MongoDB sẽ không được hỗ trợ đầy đủ. Có thể driver sẽ tự động bỏ qua các giá trị trùng lặp hoặc lưu một document không hợp lệ, dẫn đến kết quả truy vấn không nhất quán.
   - Việc cập nhật document có tên field trùng lặp cũng không được hỗ trợ, kể cả khi update có vẻ như thành công.

4. **Kiểm tra trùng lặp tên field:**
   - Từ MongoDB 6.1, bạn có thể sử dụng lệnh `validate` với tùy chọn `full: true` để kiểm tra xem document có chứa tên field trùng lặp không.
   - Ở bất kỳ phiên bản MongoDB nào, bạn có thể sử dụng toán tử aggregation `$objectToArray` để phát hiện xem một document có chứa tên field trùng lặp hay không.


### Dot Notation trong MongoDB

MongoDB sử dụng **dot notation** để truy cập các phần tử của một mảng và để truy cập các trường của một document lồng nhau (embedded document).

#### Arrays (Mảng)

Để chỉ định hoặc truy cập một phần tử trong mảng dựa trên vị trí chỉ số (bắt đầu từ 0), bạn ghép tên mảng với dấu chấm (`.`) và chỉ số phần tử, sau đó đặt trong dấu ngoặc kép:

```json
"<array>.<index>"
```


**Ví dụ:**

Giả sử bạn có một document với trường như sau:

```json
{
  ...
  "contribs": [ "Turing machine", "Turing test", "Turingery" ],
  ...
}
```

- Để truy cập phần tử thứ ba của mảng `contribs`, bạn sử dụng dot notation: `"contribs.2"`.

  

# Quản lý Databases với MongoDB Atlas UI

MongoDB Atlas UI cho phép bạn quản lý các cơ sở dữ liệu và collections trong cluster của mình thông qua giao diện đồ họa. Dưới đây là một số hướng dẫn cơ bản kèm theo vai trò cần thiết:

---

## Vai Trò Cần Thiết

| Hành động            | Vai trò yêu cầu                                                                 |
|----------------------|---------------------------------------------------------------------------------|
| **Tạo Database**     | Một trong các vai trò: Project Owner, Organization Owner, Project Data Access Admin, hoặc Project Data Access Read/Write. |
| **Xem Databases**    | Ít nhất vai trò Project Data Access Read Only.                                  |
| **Xóa Database**     | Một trong các vai trò: Project Owner hoặc Project Data Access Admin.            |

---

## Tạo Cơ Sở Dữ Liệu (Create a Database)

1. **Truy cập Clusters:**
   - Đăng nhập vào Atlas, chọn trang **Clusters** của dự án của bạn.
   - Nếu cần, chọn tổ chức và dự án từ menu **Organizations** và **Projects** trong thanh điều hướng, sau đó nhấp vào **Clusters** ở sidebar.

2. **Truy cập Collections:**
   - Nhấp nút **Browse Collections** cho cluster của bạn để mở **Data Explorer**.

3. **Tạo Database:**
   - Nhấp vào nút **Create Database**.
   - Nhập tên của Database và tên Collection đầu tiên.
   - **Lưu ý:** Không đặt tên chứa thông tin nhạy cảm.
   - Tìm hiểu thêm về [Naming Restrictions](https://docs.mongodb.com/manual/reference/limits/#naming-restrictions).

4. **Tùy Chọn Collection:**
   - **Capped Collection:** Chọn nếu muốn tạo collection với giới hạn kích thước. Sau đó chỉ định kích thước tối đa (byte).
   - **Time Series Collection:** Chọn nếu muốn tạo collection dạng time series, chỉ định time field, granularity, và tùy chọn meta field cũng như thời gian hết hạn cho dữ liệu cũ.

5. **Xác Nhận:**
   - Nhấp **Create**. Sau khi tạo thành công, Database cùng với Collection đầu tiên sẽ hiển thị trong Atlas UI.

---

## Xem Cơ Sở Dữ Liệu (View Databases)

1. **Truy cập Clusters:**
   - Đăng nhập Atlas, chọn trang **Clusters** của dự án.

2. **Truy cập Collections:**
   - Nhấp vào **Browse Collections** cho cluster của bạn để mở **Data Explorer**.
   - Tại đây, bạn có thể xem danh sách các databases và collections hiện có.

3. **Visualize Database Data:**
   - Để trực quan hóa dữ liệu, nhấp vào nút **Visualize Your Data** khi xem một database hoặc collection cụ thể.
   - Atlas sẽ mở MongoDB Charts, nơi bạn có thể xây dựng biểu đồ từ data source đã chọn. Tham khảo [Build Charts](https://docs.mongodb.com/charts/) để biết chi tiết.

---

## Xóa Cơ Sở Dữ Liệu (Drop a Database)

1. **Xóa Database:**
   - Trong Atlas UI, chọn hoặc di chuột qua Database cần xóa.
   - Nhấp vào biểu tượng thùng rác (trash can) của Database đó.

2. **Xác Nhận Hành Động:**
   - Gõ tên Database để xác nhận việc xóa.
   - Nhấp vào **Drop** để hoàn tất.

---
# Embedded Documents trong MongoDB

## Embedded Documents là gì?

Trong cơ sở dữ liệu quan hệ, bạn lưu trữ từng thực thể riêng biệt trong các bảng riêng và liên kết chúng với nhau thông qua các khóa ngoại. Mặc dù MongoDB hoàn toàn hỗ trợ tham chiếu từ document này sang document khác và thậm chí là join nhiều document, nhưng sẽ là sai lầm nếu sử dụng cơ sở dữ liệu document giống như cách bạn sử dụng cơ sở dữ liệu quan hệ.

## Ví dụ về Embedded Documents

Hãy xem xét một cấu trúc đơn giản với một người dùng và địa chỉ của họ.

### Cách tiếp cận sử dụng tham chiếu (references):

```javascript
> db.user.findOne()
{
    _id: 111111,
    email: "email@example.com",
    name: {given: "Jane", family: "Han"},
}

> db.address.find({user_id: 111111})
{
    _id: 121212,
    street: "111 Elm Street",
    city: "Springfield",
    state: "Ohio",
    country: "US",
    zip: "00000"
}
```

### Cách tiếp cận sử dụng embedded document:

```javascript
> db.user.findOne({_id: 111111})
{    
    _id: 111111,    
    email: "email@example.com",    
    name: {given: "Jane", family: "Han"},    
    address: {    
        street: "111 Elm Street",    
        city: "Springfield",    
        state: "Ohio",    
        country: "US",    
        zip: "00000",    
    }    
}
```

Bây giờ, thay vì phải thực hiện một truy vấn riêng biệt đối với collection address để lấy địa chỉ của Jane Han, bạn có thể truy cập nó như một sub-document của bản ghi người dùng.

### Lưu trữ nhiều địa chỉ:

```javascript
> db.user.findOne({_id: 111111})
{    
    _id: 111111,    
    email: "email@example.com",    
    name: {given: "Jane", family: "Han"},    
    addresses: [    
        {    
            label: "Home",    
            street: "111 Elm Street",    
            city: "Springfield",    
            state: "Ohio",    
            country: "US",    
            zip: "00000",    
        },    
        {label: "Work", ...}    
    ]    
}
```

Bạn thậm chí có thể cập nhật các địa chỉ riêng lẻ bằng toán tử vị trí (positional operator):

```javascript
> db.user.update(    
    {_id: 111111,    
    "addresses.label": "Home"},    
    {$set: {"addresses.$.street": "112 Elm Street"}}    
)
```

Lưu ý rằng bạn cần đặt bất kỳ khóa truy vấn hoặc cập nhật nào có chứa dấu chấm (như "addresses.label") trong dấu ngoặc kép để đảm bảo cú pháp chính xác. Phần truy vấn của lệnh update cần bao gồm trường mảng bạn đang cập nhật, và sau đó phần update sẽ áp dụng cho phần tử đầu tiên khớp trong mảng.

## Tại sao (và khi nào) nên ưu tiên nhúng hơn tham chiếu

Embedded documents là một cách hiệu quả và gọn gàng để lưu trữ dữ liệu liên quan, đặc biệt là dữ liệu thường xuyên được truy cập cùng nhau. Nói chung, khi thiết kế schema cho MongoDB, bạn nên ưu tiên nhúng (embedding) theo mặc định và chỉ sử dụng tham chiếu (references) và join ở phía ứng dụng hoặc cơ sở dữ liệu khi chúng thực sự cần thiết. Workload càng thường xuyên có thể truy xuất một document duy nhất và có tất cả dữ liệu cần thiết, hiệu suất ứng dụng của bạn sẽ càng ổn định và cao.

## Các mẫu nhúng phổ biến

### 1. Embedded Document Pattern

Đây là mẫu chung về việc ưu tiên nhúng ngay cả các cấu trúc phụ phức tạp vào các documents mà chúng được sử dụng cùng. Quy tắc điển hình là:

**"Những gì bạn sử dụng cùng nhau, hãy lưu trữ cùng nhau."**

### 2. Embedded Subset Pattern

Một trường hợp kết hợp, mẫu subset xuất hiện khi bạn có một collection riêng biệt cho một danh sách các item liên quan có thể rất dài, nhưng bạn muốn giữ một số item đó dễ dàng để hiển thị cho người dùng. Ví dụ:

```javascript
> db.movie.findOne()
{    
    _id: 333333,    
    title: "The Big Lebowski"
}
        
> db.review.find({movie_id: 333333})
{    
    _id: 454545,    
    movie_id: 333333,    
    stars: 3,    
    text: "it was OK"    
}    
{    
    _id: 565656,    
    movie_id: 333333,    
    stars: 5,    
    text: "the best"    
}    
...
```

Bây giờ hãy tưởng tượng bạn có hàng nghìn đánh giá, nhưng bạn luôn hiển thị hai đánh giá gần đây nhất khi hiển thị một bộ phim. Trong trường hợp này, việc lưu trữ tập con đó dưới dạng danh sách trong document movie là hợp lý.

```javascript
> db.movie.findOne({_id: 333333})
{    
    _id: 333333,    
    title: "The Big Lebowski",    
    recent_reviews: [    
        {_id: 454545, stars: 3, text: "it was OK"},    
        {_id: 565656, stars: 5, text: "the best"}    
    ]    
}
```

**Nếu bạn thường xuyên truy cập một tập con của các item liên quan, hãy nhúng tập con đó.**

### 3. Extended Reference Pattern

Một trường hợp kết hợp khác được gọi là Extended Reference. Nó khá giống với Subset Pattern, ở chỗ nó tối ưu hóa cho một lượng nhỏ thông tin thường xuyên được truy cập để lưu trữ trên document nơi nó cần. Trong trường hợp này, thay vì một danh sách, nó được sử dụng khi một document tham chiếu đến document khác trong collection riêng, nhưng cũng lưu trữ một số trường từ document khác đó để dễ truy cập.

Ví dụ:

```javascript
> db.movie.findOne({_id: 444444})
{    
    _id: 444444,    
    title: "One Flew Over the Cuckoo's Nest",    
    studio_id: 999999,    
    studio_name: "Fantasy Films"    
}
```

Như bạn có thể thấy, `studio_id` được lưu trữ để bạn có thể tra cứu thêm thông tin về studio sản xuất phim, nhưng tên của studio cũng được sao chép vào document này để dễ hiển thị. Lưu ý rằng nếu bạn đang nhúng thông tin từ các document thay đổi thường xuyên, bạn cần nhớ cập nhật các document nơi bạn đã sao chép thông tin đó khi nó thay đổi.

**Nếu bạn thường xuyên truy cập một vài trường từ document được tham chiếu, hãy nhúng các trường đó.**

## Khi nào không nên sử dụng Embedded Documents

### 1. Danh sách không giới hạn (Unbounded Lists)

Lưu trữ các danh sách ngắn thông tin liên quan trong document mà chúng thuộc về rất hợp lý, nhưng nếu danh sách của bạn có thể phát triển không kiểm soát, đặt nó trong một document duy nhất không chỉ không khôn ngoan mà còn không khả thi! MongoDB có giới hạn về kích thước của một document duy nhất, và nếu document được truy cập thường xuyên, bạn sẽ bắt đầu thấy tác động tiêu cực từ việc sử dụng bộ nhớ quá mức.

**Nếu một danh sách có thể phát triển không giới hạn, hãy đặt nó trong collection riêng.**

### 2. Truy cập độc lập (Independent Access)

Một thời điểm khác bạn nên lưu trữ sub-documents trong collection riêng là khi bạn muốn truy cập chúng độc lập với document cha mà bạn lẽ ra sẽ đặt chúng vào. Ví dụ, xem xét một sản phẩm được sản xuất bởi một công ty. Nếu công ty chỉ bán một số ít sản phẩm, bạn có thể muốn lưu trữ chúng như một phần của document công ty. Tuy nhiên, nếu bạn muốn truy cập trực tiếp các sản phẩm đó theo SKU, hoặc tái sử dụng chúng trên nhiều công ty, bạn sẽ muốn lưu trữ chúng trong collection riêng.

# Data Modeling trong MongoDB

## Data Modeling là gì?

Data modeling là việc tổ chức dữ liệu trong cơ sở dữ liệu và thiết lập các liên kết giữa các thực thể liên quan. Dữ liệu trong MongoDB có mô hình schema linh hoạt, điều này có nghĩa là:

- Documents trong cùng một collection không bắt buộc phải có cùng một tập hợp các trường.
- Kiểu dữ liệu của một trường có thể khác nhau giữa các documents trong cùng một collection.
- Nhìn chung, các documents trong một collection thường có cấu trúc tương tự. Để đảm bảo tính nhất quán trong mô hình dữ liệu của bạn, bạn có thể tạo các quy tắc schema validation.

## Các trường hợp sử dụng

Mô hình dữ liệu linh hoạt cho phép bạn tổ chức dữ liệu phù hợp với nhu cầu của ứng dụng. MongoDB là cơ sở dữ liệu document, nghĩa là bạn có thể nhúng dữ liệu liên quan vào các trường đối tượng và mảng.

Schema linh hoạt hữu ích trong các kịch bản sau:

- Công ty của bạn theo dõi nhân viên làm việc ở phòng ban nào. Bạn có thể nhúng thông tin phòng ban bên trong collection nhân viên để trả về thông tin liên quan trong một truy vấn duy nhất.

- Ứng dụng thương mại điện tử của bạn hiển thị năm đánh giá gần đây nhất khi hiển thị sản phẩm. Bạn có thể lưu trữ các đánh giá gần đây trong cùng collection với dữ liệu sản phẩm, và lưu trữ các đánh giá cũ hơn trong collection riêng biệt vì các đánh giá cũ không được truy cập thường xuyên.

- Cửa hàng quần áo của bạn cần tạo ứng dụng một trang cho danh mục sản phẩm. Các sản phẩm khác nhau có các thuộc tính khác nhau và do đó sử dụng các trường document khác nhau. Tuy nhiên, bạn có thể lưu trữ tất cả các sản phẩm trong cùng một collection.

## Thiết kế Schema: Sự khác biệt giữa cơ sở dữ liệu quan hệ và document

Khi thiết kế schema cho cơ sở dữ liệu document như MongoDB, có một số điểm khác biệt quan trọng so với cơ sở dữ liệu quan hệ:

| Cơ sở dữ liệu quan hệ | Cơ sở dữ liệu document |
|------------------------|------------------------|
| Bạn phải xác định schema của bảng trước khi chèn dữ liệu. | Schema của bạn có thể thay đổi theo thời gian khi nhu cầu của ứng dụng thay đổi. |
| Bạn thường cần join dữ liệu từ nhiều bảng khác nhau để trả về dữ liệu cần thiết cho ứng dụng. | Mô hình dữ liệu linh hoạt cho phép bạn lưu trữ dữ liệu để phù hợp với cách ứng dụng trả về dữ liệu và tránh joins. Việc tránh joins qua nhiều collections cải thiện hiệu suất và giảm tải cho triển khai của bạn. |

## Lên kế hoạch Schema

Để đảm bảo mô hình dữ liệu của bạn có cấu trúc logic và đạt hiệu suất tối ưu, hãy lên kế hoạch schema trước khi sử dụng cơ sở dữ liệu ở quy mô sản xuất. Để xác định mô hình dữ liệu, hãy sử dụng quy trình thiết kế schema sau:

1. Xác định khối lượng công việc của ứng dụng.
2. Xác định mối quan hệ giữa các đối tượng trong các collections.
3. Áp dụng các mẫu thiết kế.

## Liên kết dữ liệu liên quan

Khi thiết kế mô hình dữ liệu trong MongoDB, hãy xem xét cấu trúc của các documents và cách ứng dụng sử dụng dữ liệu từ các thực thể liên quan.

Để liên kết dữ liệu liên quan, bạn có thể:

- Nhúng dữ liệu liên quan trong một document duy nhất.
- Lưu trữ dữ liệu liên quan trong collection riêng biệt và truy cập bằng tham chiếu.

### Dữ liệu nhúng (Embedded Data)

Embedded documents lưu trữ dữ liệu liên quan trong một cấu trúc document duy nhất. Một document có thể chứa các mảng và sub-documents với dữ liệu liên quan. Các mô hình dữ liệu phi chuẩn hóa này cho phép ứng dụng truy xuất dữ liệu liên quan trong một thao tác cơ sở dữ liệu duy nhất.

*Mô hình dữ liệu với các trường nhúng chứa tất cả thông tin liên quan.*

Đối với nhiều trường hợp sử dụng trong MongoDB, mô hình dữ liệu phi chuẩn hóa là tối ưu.

Để tìm hiểu về điểm mạnh và điểm yếu của việc nhúng documents, xem phần "Embedded Data Models".

### Tham chiếu (References)

References lưu trữ mối quan hệ giữa dữ liệu bằng cách bao gồm các liên kết, gọi là tham chiếu, từ document này đến document khác. Ví dụ, trường `customerId` trong collection `orders` chỉ ra tham chiếu đến một document trong collection `customers`.

Ứng dụng có thể giải quyết các tham chiếu này để truy cập dữ liệu liên quan. Nhìn chung, đây là các mô hình dữ liệu chuẩn hóa.

*Mô hình dữ liệu sử dụng tham chiếu để liên kết documents. Cả document `contact` và document `access` đều chứa tham chiếu đến document `user`.*

Để tìm hiểu về điểm mạnh và điểm yếu của việc sử dụng tham chiếu, xem phần "References".

## Các cân nhắc bổ sung về mô hình dữ liệu

Các yếu tố sau có thể ảnh hưởng đến cách bạn lên kế hoạch mô hình dữ liệu.

### Dữ liệu trùng lặp và tính nhất quán

Khi bạn nhúng dữ liệu liên quan trong một document duy nhất, bạn có thể sao chép dữ liệu giữa hai collections. Việc sao chép dữ liệu cho phép ứng dụng truy vấn thông tin liên quan về nhiều thực thể trong một truy vấn duy nhất trong khi tách biệt các thực thể một cách hợp lý trong mô hình của bạn.

Ví dụ, collection `products` lưu trữ năm đánh giá gần đây nhất trong document sản phẩm. Những đánh giá đó cũng được lưu trữ trong collection `reviews`, chứa tất cả các đánh giá sản phẩm. Khi một đánh giá mới được viết, các thao tác ghi sau đây xảy ra:

1. Đánh giá được chèn vào collection `reviews`.
2. Mảng đánh giá gần đây trong collection `products` được cập nhật với `$pop` và `$push`.

Nếu dữ liệu trùng lặp không được cập nhật thường xuyên, thì có rất ít công việc bổ sung cần thiết để giữ cho hai collections nhất quán. Tuy nhiên, nếu dữ liệu trùng lặp được cập nhật thường xuyên, việc sử dụng tham chiếu để liên kết dữ liệu liên quan có thể là cách tiếp cận tốt hơn.

Trước khi bạn sao chép dữ liệu, hãy xem xét các yếu tố sau:

- Tần suất cập nhật dữ liệu trùng lặp.
- Lợi ích hiệu suất cho các thao tác đọc khi dữ liệu được sao chép.

Để tìm hiểu thêm, xem phần "Handle Duplicate Data".

### Indexing

Để cải thiện hiệu suất cho các truy vấn mà ứng dụng của bạn chạy thường xuyên, hãy tạo các indexes trên các trường thường được truy vấn. Khi ứng dụng phát triển, theo dõi việc sử dụng indexes để đảm bảo rằng indexes vẫn hỗ trợ các truy vấn liên quan.

### Ràng buộc phần cứng

Khi thiết kế schema, hãy xem xét phần cứng triển khai của bạn, đặc biệt là lượng RAM khả dụng. Documents lớn hơn sử dụng nhiều RAM hơn, có thể khiến ứng dụng đọc từ đĩa và làm giảm hiệu suất. Khi có thể, thiết kế schema sao cho chỉ các trường liên quan được trả về bởi các truy vấn. Phương pháp này đảm bảo rằng working set của ứng dụng không phát triển quá lớn một cách không cần thiết.

### Tính nguyên tử của Single Document

Trong MongoDB, một thao tác ghi là nguyên tử ở cấp độ của một document duy nhất, ngay cả khi thao tác sửa đổi nhiều embedded documents trong một document duy nhất. Điều này có nghĩa là nếu một thao tác cập nhật ảnh hưởng đến một số sub-documents, thì hoặc tất cả các sub-documents đó được cập nhật, hoặc thao tác hoàn toàn thất bại và không có cập nhật nào xảy ra.

Một mô hình dữ liệu phi chuẩn hóa với dữ liệu nhúng kết hợp tất cả dữ liệu liên quan trong một document duy nhất thay vì chuẩn hóa qua nhiều documents và collections. Mô hình dữ liệu này cho phép các thao tác nguyên tử, trái ngược với mô hình chuẩn hóa mà các thao tác ảnh hưởng đến nhiều documents.

Để biết thêm thông tin, xem phần "Atomicity".

# Các yếu tố hoạt động và mô hình dữ liệu trong MongoDB

Việc mô hình hóa dữ liệu ứng dụng cho MongoDB cần xem xét các yếu tố hoạt động khác nhau ảnh hưởng đến hiệu suất của MongoDB. Các mô hình dữ liệu khác nhau có thể:
- Cho phép truy vấn hiệu quả hơn
- Tăng thông lượng của các thao tác chèn và cập nhật
- Phân phối hoạt động đến cụm phân mảnh hiệu quả hơn

Khi phát triển mô hình dữ liệu, hãy phân tích tất cả các thao tác đọc và ghi của ứng dụng kết hợp với các cân nhắc sau.

## Tính nguyên tử (Atomicity)

Trong MongoDB:
- Thao tác ghi là nguyên tử ở cấp độ một tài liệu đơn lẻ, ngay cả khi thao tác sửa đổi nhiều tài liệu nhúng trong một tài liệu duy nhất
- Khi một thao tác ghi đơn lẻ sửa đổi nhiều tài liệu (ví dụ: `db.collection.updateMany()`), việc sửa đổi mỗi tài liệu là nguyên tử, nhưng thao tác nói chung thì không

### Mô hình dữ liệu nhúng

Mô hình dữ liệu nhúng kết hợp tất cả dữ liệu liên quan trong một tài liệu duy nhất thay vì chuẩn hóa trên nhiều tài liệu và bộ sưu tập. Mô hình dữ liệu này tạo điều kiện cho các thao tác nguyên tử.

### Giao dịch đa tài liệu

Đối với các mô hình dữ liệu lưu trữ tham chiếu giữa các phần dữ liệu liên quan, ứng dụng phải phát hành các thao tác đọc và ghi riêng biệt để truy xuất và sửa đổi các phần dữ liệu liên quan này.

Đối với các tình huống yêu cầu tính nguyên tử của việc đọc và ghi nhiều tài liệu (trong một hoặc nhiều bộ sưu tập), MongoDB hỗ trợ các giao dịch phân tán, bao gồm cả giao dịch trên các bộ nhân bản và các cụm phân mảnh.

> **Quan trọng**: Trong hầu hết các trường hợp, một giao dịch phân tán phát sinh chi phí hiệu suất lớn hơn so với việc ghi tài liệu đơn lẻ, và khả năng có sẵn của các giao dịch phân tán không nên là sự thay thế cho thiết kế lược đồ hiệu quả. Đối với nhiều tình huống, mô hình dữ liệu phi chuẩn hóa (tài liệu nhúng và mảng) sẽ tiếp tục là tối ưu cho dữ liệu và trường hợp sử dụng của bạn.

## Phân mảnh (Sharding)

MongoDB sử dụng phân mảnh để cung cấp khả năng mở rộng theo chiều ngang. Các cụm này hỗ trợ triển khai với các tập dữ liệu lớn và các thao tác thông lượng cao. Phân mảnh cho phép người dùng phân vùng một bộ sưu tập trong một cơ sở dữ liệu để phân phối các tài liệu của bộ sưu tập trên một số phiên bản mongod hoặc mảnh.

Để phân phối dữ liệu và lưu lượng ứng dụng trong một bộ sưu tập phân mảnh, MongoDB sử dụng khóa phân mảnh (shard key). Việc chọn khóa phân mảnh phù hợp có ý nghĩa quan trọng đối với hiệu suất, và có thể bật hoặc ngăn chặn cô lập truy vấn và tăng khả năng ghi.

## Chỉ mục (Indexes)

Sử dụng chỉ mục để cải thiện hiệu suất cho các truy vấn phổ biến. Xây dựng chỉ mục trên các trường xuất hiện thường xuyên trong các truy vấn và cho tất cả các thao tác trả về kết quả được sắp xếp. MongoDB tự động tạo một chỉ mục duy nhất trên trường `_id`.

Khi tạo chỉ mục, hãy xem xét các hành vi sau:

- Mỗi chỉ mục yêu cầu ít nhất 8 kB không gian dữ liệu
- Thêm một chỉ mục có một số tác động tiêu cực đến hiệu suất cho các thao tác ghi
- Đối với các bộ sưu tập có tỷ lệ ghi-đọc cao, chỉ mục là tốn kém vì mỗi lần chèn cũng phải cập nhật bất kỳ chỉ mục nào
- Các bộ sưu tập có tỷ lệ đọc-ghi cao thường được hưởng lợi từ các chỉ mục bổ sung
- Chỉ mục không ảnh hưởng đến các thao tác đọc không được lập chỉ mục
- Khi hoạt động, mỗi chỉ mục tiêu thụ không gian đĩa và bộ nhớ

## Số lượng lớn các bộ sưu tập

Trong một số tình huống, bạn có thể chọn lưu trữ thông tin liên quan trong một số bộ sưu tập thay vì trong một bộ sưu tập duy nhất.

Ví dụ về bộ sưu tập logs:

```javascript
{ log: "dev", ts: ..., info: ... }
{ log: "debug", ts: ..., info: ...}
```

Nếu tổng số tài liệu thấp, bạn có thể nhóm tài liệu vào bộ sưu tập theo loại, như `logs_dev` và `logs_debug`.

Khi sử dụng mô hình có số lượng lớn bộ sưu tập, hãy xem xét:

- Mỗi bộ sưu tập có một mức tối thiểu nhất định của chi phí vài kilobyte
- Mỗi chỉ mục, bao gồm cả chỉ mục trên `_id`, yêu cầu ít nhất 8 kB không gian dữ liệu
- Đối với mỗi cơ sở dữ liệu, một tệp không gian tên duy nhất (tức là `<database>.ns`) lưu trữ tất cả dữ liệu meta cho cơ sở dữ liệu đó

## Bộ sưu tập chứa số lượng lớn tài liệu nhỏ

Bạn nên xem xét nhúng vì lý do hiệu suất nếu bạn có một bộ sưu tập với số lượng lớn tài liệu nhỏ. Nếu bạn có thể nhóm các tài liệu nhỏ này theo một số mối quan hệ hợp lý và bạn thường xuyên truy xuất tài liệu theo nhóm này, bạn có thể xem xét "cuộn lên" (rolling-up) các tài liệu nhỏ thành tài liệu lớn hơn chứa một mảng các tài liệu nhúng.

Lợi ích:
- Truy vấn để truy xuất một nhóm tài liệu liên quan đến đọc tuần tự và ít truy cập đĩa ngẫu nhiên hơn
- Có ít bản sao hơn của các trường chung và ít mục nhập khóa liên quan hơn trong chỉ mục tương ứng

Tuy nhiên, nếu bạn thường chỉ cần truy xuất một tập con của tài liệu trong nhóm, thì "cuộn lên" có thể không cải thiện hiệu suất.

## Tối ưu hóa lưu trữ cho tài liệu nhỏ

Mỗi tài liệu MongoDB chứa một lượng chi phí nhất định. Chi phí này thường không đáng kể nhưng trở nên đáng kể nếu tất cả tài liệu chỉ có vài byte.

Các chiến lược tối ưu hóa:

### Sử dụng trường `_id` một cách rõ ràng

MongoDB tự động thêm trường `_id` vào mỗi tài liệu và tạo một ObjectId 12-byte duy nhất. Để tối ưu hóa việc sử dụng lưu trữ, người dùng có thể chỉ định một giá trị cho trường `_id` khi chèn tài liệu vào bộ sưu tập.

### Sử dụng tên trường ngắn hơn

Ví dụ, thay vì:
```javascript
{ last_name: "Smith", best_score: 3.9 }
```

Bạn có thể sử dụng:
```javascript
{ lname: "Smith", score: 3.9 }
```

Điều này có thể tiết kiệm 9 byte cho mỗi tài liệu.

> **Lưu ý**: Việc rút ngắn tên trường làm giảm tính biểu đạt và không mang lại lợi ích đáng kể cho các tài liệu lớn hơn. Tên trường ngắn hơn không làm giảm kích thước của chỉ mục.

### Nhúng tài liệu

Trong một số trường hợp, bạn có thể muốn nhúng tài liệu vào tài liệu khác để tiết kiệm chi phí cho mỗi tài liệu.

## Quản lý vòng đời dữ liệu

Các quyết định mô hình hóa dữ liệu nên xem xét việc quản lý vòng đời dữ liệu:

- Tính năng **Time to Live (TTL)** của bộ sưu tập giúp hết hạn tài liệu sau một khoảng thời gian
- **Bộ sưu tập giới hạn** (Capped Collections) cung cấp quản lý first-in-first-out (FIFO) của tài liệu đã chèn và hỗ trợ hiệu quả các thao tác chèn và đọc tài liệu dựa trên thứ tự chèn

---
# Connecting to a MongoDB Database

# Connection Strings

> Sử dụng menu thả xuống "Select your language" ở góc trên bên phải để cài đặt ngôn ngữ cho các ví dụ sau.

Bạn có thể sử dụng connection strings để định nghĩa kết nối giữa các instance MongoDB và các đích đến sau:

- Ứng dụng của bạn khi kết nối sử dụng drivers.
- Công cụ như MongoDB Compass và MongoDB Shell (mongosh).

## Tương thích

Bạn có thể sử dụng connection strings để kết nối đến các deployment được host trong các môi trường sau:

- **MongoDB Atlas**: Dịch vụ được quản lý hoàn toàn cho các deployment MongoDB trên cloud
- **MongoDB Enterprise**: Phiên bản MongoDB dựa trên đăng ký, tự quản lý
- **MongoDB Community**: Phiên bản MongoDB nguồn mở, miễn phí sử dụng và tự quản lý

Hoàn thành các bước sau để tìm connection string của bạn.

## Tìm MongoDB Atlas Connection String

### Atlas CLI

**Atlas UI**  
Để tìm MongoDB Atlas connection string bằng Atlas CLI, hãy cài đặt và kết nối từ Atlas CLI, sau đó chạy lệnh sau. Thay `<clusterName>` bằng tên của MongoDB Atlas cluster và thay `<projectId>` bằng project ID.

```
atlas clusters connectionStrings describe <clusterName> --projectId <projectId>
```

Để tìm hiểu thêm, xem `atlas clusters connectionStrings describe`.

MongoDB Atlas connection string của bạn sẽ giống như ví dụ sau:

```
mongodb+srv://myDatabaseUser:D1fficultP%40ssw0rd@cluster0.example.mongodb.net/?retryWrites=true&w=majority
```

## Tìm Connection String cho Self-Hosted Deployment

Nếu bạn đã kết nối với MongoDB Enterprise hoặc MongoDB Community deployment tự host, hãy chạy phương thức `db.getMongo()` để trả về connection string.

Nếu bạn không kết nối với deployment, bạn có thể xác định connection string dựa trên loại kết nối bạn muốn sử dụng. Xem **SRV Connection Format** để tìm hiểu cú pháp connection string SRV hoặc **Standard Connection String Format** để tìm hiểu cú pháp connection string tiêu chuẩn.

Connection string tự host của bạn sẽ giống các ví dụ sau:

### SRV Connection String

### Standard Connection String

### Replica Set

### Sharded Cluster

### Standalone

Connection string replica set sau bao gồm các thành phần:
- Tùy chọn `replicaSet`
- Hostname của (các) instance mongod như được liệt kê trong cấu hình replica set
- Nó xác thực với user `myDatabaseUser` với mật khẩu `D1fficultP%40ssw0rd` để thực thi kiểm soát truy cập

```
mongodb+srv://myDatabaseUser:D1fficultP%40ssw0rd@mongodb0.example.com/?authSource=admin&replicaSet=myRepl
```

Nếu tên người dùng hoặc mật khẩu bao gồm các ký tự sau, những ký tự đó phải được chuyển đổi bằng percent encoding:

```
$ : / ? # [ ] @
```

Để biết danh sách đầy đủ các tùy chọn connection string, xem **SRV Connection Format** hoặc **Standard Connection String Format**. Để xem thêm ví dụ, xem **Connection String Examples**.

## Connection String Formats

Bạn có thể chỉ định MongoDB connection string bằng một trong các định dạng sau:

- **SRV Connection Format**: Connection string với hostname tương ứng với DNS SRV record. Driver hoặc mongosh của bạn truy vấn record để xác định máy chủ nào đang chạy các instance mongod hoặc mongos.
- **Standard Connection String Format**: Connection string chỉ định tất cả các máy chủ đang chạy các instance mongod hoặc mongos.

MongoDB Atlas clusters sử dụng SRV connection format trừ khi bạn kết nối đến online archive.

### SRV Connection Format

MongoDB hỗ trợ danh sách seed được xây dựng từ DNS. Sử dụng DNS để xây dựng danh sách máy chủ khả dụng cho phép triển khai linh hoạt hơn và khả năng thay đổi các máy chủ trong rotation mà không cần cấu hình lại clients.

URI connection scheme SRV có dạng sau:

```
mongodb+srv://[username:password@]host[/[defaultauthdb][?options]]
```

Để xem thêm ví dụ, xem **Connection String Examples**.

#### Connection String Components

Connection string bao gồm các thành phần sau:

| Thành phần | Mô tả |
|------------|-------|
| mongodb:// hoặc mongodb+srv:// | Tiền tố bắt buộc để xác định đây là chuỗi ở định dạng kết nối tiêu chuẩn (mongodb://) hoặc định dạng kết nối SRV (mongodb+srv://). Để tìm hiểu thêm về từng định dạng, xem **Standard Connection String Format** và **SRV Connection Format**. |
| username:password@ | Tùy chọn. Thông tin xác thực.<br><br>Nếu được chỉ định, client sẽ cố gắng xác thực người dùng với authSource. Nếu authSource không được chỉ định, client sẽ cố gắng xác thực người dùng với defaultauthdb. Và nếu defaultauthdb không được chỉ định, sẽ xác thực với database admin.<br><br>Nếu tên người dùng hoặc mật khẩu bao gồm các ký tự sau, những ký tự đó phải được chuyển đổi bằng percent encoding:<br><br>$ : / ? # [ ] @<br><br>Xem thêm authSource. |
| host[:port] | Máy chủ (và số cổng tùy chọn) nơi instance mongod (hoặc instance mongos cho sharded cluster) đang chạy. Bạn có thể chỉ định hostname, địa chỉ IP hoặc UNIX domain socket. Chỉ định càng nhiều máy chủ càng tốt cho topo triển khai của bạn:<br><br>- Đối với standalone, chỉ định hostname của instance mongod standalone.<br>- Đối với replica set, chỉ định hostname của (các) instance mongod như được liệt kê trong cấu hình replica set.<br>- Đối với sharded cluster, chỉ định hostname của (các) instance mongos.<br><br>Nếu số cổng không được chỉ định, cổng mặc định 27017 được sử dụng.<br><br>Nếu bạn sử dụng định dạng kết nối SRV URI, bạn chỉ có thể chỉ định một máy chủ và không có cổng. Nếu không, driver hoặc mongosh sẽ báo lỗi phân tích và không thực hiện phân giải DNS. |
| /defaultauthdb | Tùy chọn. Cơ sở dữ liệu xác thực sẽ sử dụng nếu connection string bao gồm thông tin xác thực username:password@ nhưng tùy chọn authSource không được chỉ định.<br><br>Nếu cả authSource và defaultauthdb đều không được chỉ định, client sẽ cố gắng xác thực người dùng đã chỉ định với cơ sở dữ liệu admin. |
| ?<options> | Tùy chọn. Chuỗi truy vấn chỉ định các tùy chọn kết nối cụ thể dưới dạng các cặp <name>=<value>. Xem **Connection String Options** để biết mô tả đầy đủ về các tùy chọn này.<br><br>Nếu connection string không chỉ định database/ bạn phải chỉ định dấu gạch chéo (/) giữa máy chủ cuối cùng và dấu hỏi (?) bắt đầu chuỗi các tùy chọn. |

Để tận dụng danh sách seed DNS, hãy sử dụng cú pháp tương tự như connection string tiêu chuẩn với tiền tố là `mongodb+srv` thay vì `mongodb` tiêu chuẩn. `+srv` chỉ định cho client rằng hostname theo sau tương ứng với DNS SRV record. Driver hoặc mongosh sau đó sẽ truy vấn DNS cho record để xác định máy chủ nào đang chạy các instance mongod hoặc mongos.

> **Lưu ý**: Việc sử dụng bổ ngữ connection string `+srv` tự động đặt tùy chọn tls (hoặc tùy chọn tương đương ssl) thành true cho kết nối. Bạn có thể ghi đè hành vi này bằng cách đặt rõ ràng tùy chọn tls (hoặc tùy chọn tương đương ssl) thành false với tls=false (hoặc ssl=false) trong chuỗi truy vấn.

Khi sử dụng định dạng `+srv`, bạn phải chỉ định hostname, domain và top-level domain (TLD) theo định dạng sau: `<hostname>.<domain>.<TLD>`. Bảng này cho thấy các placeholder tương ứng với các giá trị ví dụ:

| Placeholder | Ví dụ |
|-------------|-------|
| <hostname> | server |
| <domain> | example |
| <TLD> | com |
| <hostname>.<domain>.<TLD> | server.example.com |

Ví dụ này hiển thị connection string danh sách seed DNS sử dụng đúng định dạng `<hostname>.<domain>.<TLD>`. Nó xác thực là người dùng myDatabaseUser với mật khẩu D1fficultP%40ssw0rd:

```
mongodb+srv://myDatabaseUser:D1fficultP%40ssw0rd@server.example.com/
```

Cấu hình DNS tương ứng giống như:

```
Record                            TTL   Class    Priority Weight Port  Target
_mongodb._tcp.server.example.com. 86400 IN SRV   0        5      27317 mongodb1.example.com.
_mongodb._tcp.server.example.com. 86400 IN SRV   0        5      27017 mongodb2.example.com.
```

Các bản ghi SRV riêng lẻ phải có định dạng `_mongodb._tcp.<hostname>.<domain>.<TLD>`.

Khi client kết nối với một thành viên của danh sách seed, client sẽ truy xuất danh sách các thành viên replica set mà nó có thể kết nối. Clients thường sử dụng DNS aliases trong danh sách seed của họ, điều này có nghĩa là máy chủ có thể trả về danh sách server khác với danh sách seed ban đầu. Nếu điều này xảy ra, clients sẽ sử dụng hostnames được cung cấp bởi replica set thay vì hostnames được liệt kê trong danh sách seed để đảm bảo rằng các thành viên replica set có thể được truy cập thông qua hostnames trong cấu hình replica set kết quả.

> **Quan trọng**: Các hostnames được trả về trong bản ghi SRV phải có cùng parent domain (trong ví dụ này là example.com) với hostname đã cho. Nếu parent domains và hostname không khớp, bạn sẽ không thể kết nối.

Ví dụ này hiển thị connection string danh sách seed DNS thiếu `<hostname>`. Điều này không chính xác và gây ra lỗi.

```
# Connection string này thiếu <hostname> và gây ra lỗi kết nối
mongodb+srv://myDatabaseUser:D1fficultP%40ssw0rd@example.com/
```

Giống như connection string tiêu chuẩn, connection string danh sách seed DNS hỗ trợ chỉ định các tùy chọn dưới dạng chuỗi truy vấn. Với connection string danh sách seed DNS, bạn cũng có thể chỉ định các tùy chọn sau thông qua TXT record:

- replicaSet
- authSource

Bạn chỉ có thể chỉ định một TXT record cho mỗi instance mongod. Nếu nhiều TXT records xuất hiện trong DNS và/hoặc nếu TXT record chứa tùy chọn khác ngoài replicaSet hoặc authSource, client sẽ trả về lỗi.

TXT record cho mục DNS server.example.com sẽ giống như:

```
Record              TTL   Class    Text
server.example.com. 86400 IN TXT   "replicaSet=mySet&authSource=authDB"
```

Kết hợp lại, các bản ghi DNS SRV và các tùy chọn được chỉ định trong TXT record sẽ giải quyết thành connection string định dạng tiêu chuẩn sau:

```
mongodb://myDatabaseUser:D1fficultP%40ssw0rd@mongodb1.example.com:27317,mongodb2.example.com:27017/?replicaSet=mySet&authSource=authDB
```

Bạn có thể ghi đè các tùy chọn được chỉ định trong TXT record bằng cách truyền tùy chọn trong chuỗi truy vấn. Trong ví dụ sau, chuỗi truy vấn đã cung cấp một override cho tùy chọn authSource được cấu hình trong TXT record của mục DNS ở trên.

```
mongodb+srv://myDatabaseUser:D1fficultP%40ssw0rd@server.example.com/?connectTimeoutMS=300000&authSource=aDifferentAuthDB
```

Với override cho authSource, connection string tương đương ở định dạng tiêu chuẩn sẽ là:

```
mongodb://myDatabaseUser:D1fficultP%40ssw0rd@mongodb1.example.com:27317,mongodb2.example.com:27017/?connectTimeoutMS=300000&replicaSet=mySet&authSource=aDifferentAuthDB
```

> **Lưu ý**: Tùy chọn mongodb+srv sẽ thất bại nếu không có DNS khả dụng với các bản ghi tương ứng với hostname được xác định trong connection string. Nếu bạn sử dụng bổ ngữ connection string +srv, tùy chọn tls (hoặc tùy chọn tương đương ssl) sẽ được đặt thành true cho kết nối. Bạn có thể ghi đè hành vi này bằng cách đặt rõ ràng tùy chọn tls (hoặc tùy chọn tương đương ssl) thành false với tls=false (hoặc ssl=false) trong chuỗi truy vấn.

Để biết ví dụ về việc kết nối mongosh với replica set bằng định dạng kết nối danh sách seed DNS, xem **mongosh Connection Options**.

### Standard Connection String Format

Phần này mô tả định dạng tiêu chuẩn của MongoDB connection URI được sử dụng để kết nối với MongoDB standalone deployment, replica set hoặc sharded cluster tự host.

Schema kết nối URI tiêu chuẩn có dạng:

```
mongodb://[username:password@]host1[:port1][,...hostN[:portN]][/[defaultauthdb][?options]]
```

Để xem thêm ví dụ, xem **Connection String Examples**.

#### Connection String Database Options

Bạn có thể chỉ định cơ sở dữ liệu mặc định trong trường [/defaultauthdb] của connection string. Client sử dụng cơ sở dữ liệu [/defaultauthdb] được chỉ định làm cơ sở dữ liệu mặc định. Nếu không được chỉ định bởi connection string, cơ sở dữ liệu mặc định là cơ sở dữ liệu test.

Bạn có thể chỉ định cơ sở dữ liệu xác thực trong connection string của bạn bằng tùy chọn kết nối authSource. Nếu được chỉ định, client sử dụng cơ sở dữ liệu này để xác minh danh tính và thông tin đăng nhập của bạn. Nếu authSource không được chỉ định, nó mặc định là cơ sở dữ liệu [/defaultauthdb]. Nếu cả authSource và [/defaultauthdb] đều không được chỉ định, authSource mặc định là cơ sở dữ liệu admin.

Connection string sau đặt cơ sở dữ liệu mặc định thành myDefaultDB và cơ sở dữ liệu xác thực thành admin:

```
mongodb://myDatabaseUser:D1fficultP%40ssw0rd@mongodb0.example.com:27017/myDefaultDB?authSource=admin
```

#### Connection String Components

Connection string bao gồm các thành phần sau:

| Thành phần | Mô tả |
|------------|-------|
| mongodb:// hoặc mongodb+srv:// | Tiền tố bắt buộc để xác định đây là chuỗi ở định dạng kết nối tiêu chuẩn (mongodb://) hoặc định dạng kết nối SRV (mongodb+srv://). Để tìm hiểu thêm về từng định dạng, xem **Standard Connection String Format** và **SRV Connection Format**. |
| username:password@ | Tùy chọn. Thông tin xác thực.<br><br>Nếu được chỉ định, client sẽ cố gắng xác thực người dùng với authSource. Nếu authSource không được chỉ định, client sẽ cố gắng xác thực người dùng với defaultauthdb. Và nếu defaultauthdb không được chỉ định, sẽ xác thực với database admin.<br><br>Nếu tên người dùng hoặc mật khẩu bao gồm các ký tự sau, những ký tự đó phải được chuyển đổi bằng percent encoding:<br><br>$ : / ? # [ ] @<br><br>Xem thêm authSource. |
| host[:port] | Máy chủ (và số cổng tùy chọn) nơi instance mongod (hoặc instance mongos cho sharded cluster) đang chạy. Bạn có thể chỉ định hostname, địa chỉ IP hoặc UNIX domain socket. Chỉ định càng nhiều máy chủ càng tốt cho topo triển khai của bạn:<br><br>- Đối với standalone, chỉ định hostname của instance mongod standalone.<br>- Đối với replica set, chỉ định hostname của (các) instance mongod như được liệt kê trong cấu hình replica set.<br>- Đối với sharded cluster, chỉ định hostname của (các) instance mongos.<br><br>Nếu số cổng không được chỉ định, cổng mặc định 27017 được sử dụng.<br><br>Nếu bạn sử dụng định dạng kết nối SRV URI, bạn chỉ có thể chỉ định một máy chủ và không có cổng. Nếu không, driver hoặc mongosh sẽ báo lỗi phân tích và không thực hiện phân giải DNS. |
| /defaultauthdb | Tùy chọn. Cơ sở dữ liệu xác thực sẽ sử dụng nếu connection string bao gồm thông tin xác thực username:password@ nhưng tùy chọn authSource không được chỉ định.<br><br>Nếu cả authSource và defaultauthdb đều không được chỉ định, client sẽ cố gắng xác thực người dùng đã chỉ định với cơ sở dữ liệu admin. |
| ?<options> | Tùy chọn. Chuỗi truy vấn chỉ định các tùy chọn kết nối cụ thể dưới dạng các cặp <name>=<value>. Xem **Connection String Options** để biết mô tả đầy đủ về các tùy chọn này.<br><br>Nếu connection string không chỉ định database/ bạn phải chỉ định dấu gạch chéo (/) giữa máy chủ cuối cùng và dấu hỏi (?) bắt đầu chuỗi các tùy chọn. |

---
# Connecting to MongoDB in Python

```bash
pip install 'pymongo[srv]'
```
