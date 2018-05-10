'use strict';

module.exports = (sequelize, DataTypes) => {
  var Model = sequelize.define('auth_permission', {
    'name': {
      type: DataTypes.STRING,
    },
    'codename': {
      type: DataTypes.STRING,
    },
  }, {
    tableName: 'auth_permission',
    
    timestamps: false,
    schema: process.env.DATABASE_SCHEMA,
  });

  Model.associate = (models) => {
    Model.belongsTo(models.django_content_type, {
      foreignKey: 'content_type_id',
      
      as: '_content_type_id',
    });
    
  };

  return Model;
};

