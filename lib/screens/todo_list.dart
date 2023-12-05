import 'package:flutter/material.dart';
import 'package:todo_app/screens/add_page.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';



class TodoListPage extends StatefulWidget {

  const TodoListPage({Key? key}) : super(key: key);


  @override
  State<TodoListPage> createState() => _TodoListPageState();
}

class _TodoListPageState extends State<TodoListPage> {

  List items = [];

  @override
  void initState() {
    super.initState();
    fetchTodos();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Center(child: Text("Todo List")),
      ),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: () {
          navigateToAddPage();
        },
        label: Text("Add Todo"), 
      ),
      body: RefreshIndicator(
        onRefresh: fetchTodos,
        child: ListView.builder(
          itemCount: items.length,
          itemBuilder: (context, index) {
            final item = items[index];
            final id = item['id'];
            return ListTile(
              leading: CircleAvatar(child: Text('${index + 1}')),
              title: Text(item['text']),
              subtitle: Text(item['desc'] != null ? item['desc'] : ''),
              trailing: PopupMenuButton(
                itemBuilder: (context) => [
                  PopupMenuItem(
                    child: Text('Edit'),
                    value: 'edit',
                  ),
                  PopupMenuItem(
                    child: Text('Delete'),
                    value: 'delete',
                  ),
                ],
                onSelected: (value) {
                  if(value == 'edit') {
                    print('Edit');
                    navigateToEditPage(item);
                  } else if(value == 'delete') {
                    print('Delete');
                    deleteById(id);
                  }
                },
              ),
            );
          },
        )
      )
    );
  }

  Future<void> navigateToAddPage() async {
    final route = MaterialPageRoute(builder: (context) => AddTodoPage());
    await Navigator.push(context, route);
    fetchTodos();
  }

  Future<void> navigateToEditPage(Map item) async {
    final route = MaterialPageRoute(builder: (context) => AddTodoPage());
    await Navigator.push(context, route);
    fetchTodos();
  }



  Future<void> deleteById(String id) async {
    final response = await http.delete(Uri.parse('http://localhost:5000/items/$id'));

    if(response.statusCode == 200) {
      print('Deleted');
      final filtered = items.where((item) => item['id'] != id).toList();

      setState(() {
        items = filtered;
      });

    } else {
      print('Failed to delete');
    }
  }

  Future<void> fetchTodos() async {
    final response = await http.get(Uri.parse('http://localhost:5000/items'));

    if(response.statusCode == 200) {
      final todos = jsonDecode(response.body) as Map;
      final json = todos['items'] as List;
      print(json);

        setState(() {
            items = json;
        }); 

    } else {
      print('Failed to fetch todos');
    }
  }

}